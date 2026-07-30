import copy
import json
import logging
import re

from ..ai_review.ollama_client import OllamaClient, OllamaClientError
from .prompt_builder import CodeQualityPromptBuilder
from .schemas import CodeQualityResponseSchema

logger = logging.getLogger(__name__)

FALLBACK_QUALITY_REVIEW = {
    'score': 78,
    'summary': (
        'تعذّر إكمال تحليل الجودة الكامل حالياً. '
        'يمكنك الاعتماد على هذا التقييم المؤقت ثم إعادة المحاولة لاحقاً.'
    ),
    'complexity': {
        'time': 'تعقيد زمني تقريبي غير مؤكد؛ أعد المحاولة للحصول على تحليل أدق.',
        'space': 'تعقيد مساحي تقريبي غير مؤكد؛ أعد المحاولة للحصول على تحليل أدق.',
    },
    'strengths': [
        'الحل اجتاز الاختبارات بنجاح، وهذا أساس جيد لمراجعة الجودة.',
    ],
    'clean_code_tips': [
        'راجع أسماء المتغيرات والدوال وهل تعبّر بوضوح عن الغرض.',
        'قسّم المنطق الطويل إلى وحدات أصغر يسهل فهمها وصيانتها.',
    ],
    'performance_tips': [
        'ابحث عن التكرار غير الضروري في الحلقات أو العمليات المكلفة.',
        'فكّر هل يمكن تقليل العمل المكرر دون تغيير صحة النتيجة.',
    ],
}


class CodeQualityReviewService:
    """Service for post-success AI code quality review.

    Builds a quality-focused prompt, calls Ollama through the shared
    OllamaClient, validates the structured response, and never returns
    untrusted AI output directly to the API.
    """

    def __init__(self, client=None, prompt_builder=None):
        self.client = client or OllamaClient()
        self.prompt_builder = prompt_builder or CodeQualityPromptBuilder()

    def review(self, project, files, test_summary=None):
        prompt_parts = self.prompt_builder.build(
            project=project,
            files=files,
            test_summary=test_summary,
        )

        try:
            raw_response = self.client.review(
                system=prompt_parts.get('system'),
                user=prompt_parts.get('user'),
            )
        except OllamaClientError as exc:
            logger.warning('Code quality review request failed: %s', exc)
            return self._fallback_response()

        review_data = self._parse_and_validate(raw_response)
        if review_data is None:
            return self._fallback_response()

        return {
            'success': True,
            'review': review_data,
        }

    def _parse_and_validate(self, raw_response):
        try:
            payload = self._extract_json(raw_response)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.warning('Code quality AI returned invalid JSON: %s', exc)
            return None

        if not isinstance(payload, dict):
            logger.warning(
                'Code quality response JSON must be an object, got %s',
                type(payload).__name__,
            )
            return None

        # Accept alternate key names from the model and normalize.
        payload = self._normalize_payload(payload)

        serializer = CodeQualityResponseSchema(data=payload)
        if not serializer.is_valid():
            logger.warning(
                'Code quality response failed schema validation: %s',
                serializer.errors,
            )
            return None

        return serializer.validated_data

    def _normalize_payload(self, payload):
        data = dict(payload)

        if 'score' not in data and 'overall_score' in data:
            data['score'] = data.get('overall_score')

        complexity = data.get('complexity')
        if isinstance(complexity, dict):
            normalized = dict(complexity)
            if 'time' not in normalized and 'time_complexity' in normalized:
                normalized['time'] = normalized.get('time_complexity')
            if 'space' not in normalized and 'space_complexity' in normalized:
                normalized['space'] = normalized.get('space_complexity')
            data['complexity'] = normalized
        elif isinstance(complexity, str) and complexity.strip():
            data['complexity'] = {
                'time': complexity.strip(),
                'space': complexity.strip(),
            }

        for key in ('strengths', 'clean_code_tips', 'performance_tips'):
            value = data.get(key)
            if value is None:
                data[key] = []
            elif isinstance(value, str):
                data[key] = [value] if value.strip() else []

        return data

    def _extract_json(self, raw_response):
        if raw_response is None:
            raise ValueError('Empty AI response')

        cleaned = str(raw_response).strip()
        if not cleaned:
            raise ValueError('Empty AI response')

        if cleaned.startswith('```'):
            cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            if start == -1 or end == -1 or end <= start:
                raise
            return json.loads(cleaned[start:end + 1])

    def _fallback_response(self):
        return {
            'success': True,
            'review': copy.deepcopy(FALLBACK_QUALITY_REVIEW),
        }
