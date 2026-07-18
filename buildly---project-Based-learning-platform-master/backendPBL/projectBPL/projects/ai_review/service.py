import copy
import json
import logging
import re

from .ollama_client import OllamaClient, OllamaClientError
from .prompt_builder import PromptBuilder
from .schemas import AIReviewResponseSchema

logger = logging.getLogger(__name__)

FALLBACK_REVIEW = {
    'overall_score': 85,
    'summary': 'Temporary review.',
    'strengths': [
        'Good project structure',
    ],
    'issues': [
        {
            'id': 1,
            'category': 'Readability',
            'severity': 'Medium',
            'file': 'main.py',
            'line': 10,
            'title': 'Example Issue',
            'explanation': 'Temporary explanation.',
            'hint': 'Temporary hint.',
        }
    ],
}

FAILED_TESTS_EMPTY_ISSUES_FALLBACK = {
    'overall_score': 35,
    'summary': (
        'لا تزال بعض متطلبات المشروع غير مكتملة وفق نتائج Check Code. '
        'راجع المتطلبات الفاشلة وفكّر في سبب عدم تطابق سلوك البرنامج معها.'
    ),
    'strengths': [],
    'issues': [
        {
            'id': 1,
            'category': 'Logic',
            'severity': 'High',
            'file': 'workspace',
            'line': 1,
            'title': 'متطلبات المشروع ما زالت تفشل في الاختبارات',
            'explanation': (
                'نتائج الاختبارات تظهر أن جزءاً من قصص المستخدم/المتطلبات لم يُحقَّق بعد. '
                'هذا يعني أن السلوك الحالي لا يغطي ما يتوقعه المشروع، حتى لو بدا الكود مرتباً. '
                'لا يكفي الاعتماد على مظهر الكود وحده؛ ركّز على الفجوة بين ما يفعله البرنامج '
                'وما تطلبه المتطلبات الفاشلة.'
            ),
            'hint': (
                'أعد قراءة كل متطلب فاشل، ثم اسأل نفسك: أي جزء من السلوك المتوقع لم يظهر؟ '
                'قارن المدخلات/المخرجات المتوقعة مع ما يحدث فعلياً، وصحّح المنطق خطوة بخطوة '
                'دون نسخ حل جاهز.'
            ),
        }
    ],
}


class AIReviewService:
    """Service for AI code review.

    Builds the final prompt via PromptBuilder, calls Ollama through
    OllamaClient, validates the structured response, and never returns
    untrusted AI output directly to the API.
    """

    def __init__(self, client=None, prompt_builder=None):
        self.client = client or OllamaClient()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def review(
        self,
        project,
        files,
        test_summary=None,
        failed_tests=None,
        test_error=None,
    ):
        prompt = self.prompt_builder.build(
            project=project,
            files=files,
            test_summary=test_summary,
            failed_tests=failed_tests,
            test_error=test_error,
        )

        try:
            raw_response = self.client.review(prompt)
        except OllamaClientError as exc:
            logger.warning('AI review request failed: %s', exc)
            return self._fallback_response(test_summary=test_summary, failed_tests=failed_tests)

        review_data = self._parse_and_validate(raw_response)
        if review_data is None:
            return self._fallback_response(test_summary=test_summary, failed_tests=failed_tests)

        review_data = self._guard_failed_tests_review(
            review_data,
            test_summary=test_summary,
            failed_tests=failed_tests,
        )

        return {
            'success': True,
            'review': review_data,
        }

    def _failed_count(self, test_summary):
        if not test_summary:
            return 0
        if isinstance(test_summary, dict) or hasattr(test_summary, 'get'):
            return int(test_summary.get('failed', 0) or 0)
        return int(getattr(test_summary, 'failed', 0) or 0)

    def _guard_failed_tests_review(self, review_data, test_summary=None, failed_tests=None):
        failed_count = self._failed_count(test_summary)
        if failed_count <= 0:
            return review_data

        issues = review_data.get('issues') or []
        if not issues:
            logger.warning(
                'AI returned empty issues while failed tests=%s; applying educational fallback',
                failed_count,
            )
            return self._build_failed_tests_fallback(failed_tests=failed_tests, failed_count=failed_count)

        score = int(review_data.get('overall_score') or 0)
        if score > 45:
            review_data['overall_score'] = 45

        return review_data

    def _build_failed_tests_fallback(self, failed_tests=None, failed_count=0):
        review = copy.deepcopy(FAILED_TESTS_EMPTY_ISSUES_FALLBACK)
        review['summary'] = (
            f'فشل {failed_count} من اختبارات/متطلبات المشروع. '
            'راجع المشكلات أدناه لفهم الفجوة المنطقية دون طلب الحل الكامل.'
        )

        issues = []
        failed_tests = failed_tests or []
        for index, item in enumerate(failed_tests, start=1):
            if isinstance(item, dict) or hasattr(item, 'get'):
                getter = item.get
            else:
                getter = lambda key, default='': getattr(item, key, default)

            name = (getter('name', '') or '').strip()
            requirement = (getter('requirement', '') or '').strip()
            message = (getter('message', '') or '').strip()
            title = name or (requirement[:80] if requirement else f'متطلب فاشل {index}')

            explanation_parts = [
                'ما زال هذا المتطلب يفشل وفق نتائج Check Code.',
            ]
            if requirement:
                explanation_parts.append(f'المتطلب: {requirement}')
            if message:
                explanation_parts.append(f'رسالة الاختبار: {message}')
            explanation_parts.append(
                'ركّز على سبب عدم تطابق سلوك البرنامج مع هذا المتطلب، '
                'دون كتابة كود جاهز أو كشف الحل النهائي.'
            )

            issues.append(
                {
                    'id': index,
                    'category': 'Logic',
                    'severity': 'High',
                    'file': 'workspace',
                    'line': 1,
                    'title': title,
                    'explanation': ' '.join(explanation_parts),
                    'hint': (
                        'حدّد ما الذي يتوقعه المتطلب وما الذي يحدث فعلياً، '
                        'ثم عدّل المنطق تدريجياً حتى يمر الاختبار.'
                    ),
                }
            )

        if issues:
            review['issues'] = issues
        return review

    def _parse_and_validate(self, raw_response):
        try:
            payload = self._extract_json(raw_response)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.warning('AI returned invalid JSON: %s', exc)
            return None

        if not isinstance(payload, dict):
            logger.warning('AI response JSON must be an object, got %s', type(payload).__name__)
            return None

        serializer = AIReviewResponseSchema(data=payload)
        if not serializer.is_valid():
            logger.warning('AI response failed schema validation: %s', serializer.errors)
            return None

        return serializer.validated_data

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

    def _fallback_response(self, test_summary=None, failed_tests=None):
        if self._failed_count(test_summary) > 0:
            return {
                'success': True,
                'review': self._build_failed_tests_fallback(
                    failed_tests=failed_tests,
                    failed_count=self._failed_count(test_summary),
                ),
            }

        return {
            'success': True,
            'review': copy.deepcopy(FALLBACK_REVIEW),
        }
