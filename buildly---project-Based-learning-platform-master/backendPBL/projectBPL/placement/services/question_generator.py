import json
import logging
import re
import urllib.error
import urllib.request

from django.conf import settings

from placement.constants import DIFFICULTY_SCORES, ability_to_difficulty_level
from placement.track_config import get_track_config, get_track_topics

logger = logging.getLogger(__name__)

DIFFICULTY_GUIDANCE = {
    'beginner': 'أساسيات المفاهيم والبنية',
    'intermediate': 'سلوك اللغة، الأنماط الشائعة، والتطبيق العملي',
    'advanced': 'حالات متقدمة، أداء، وأنماط حديثة',
    'expert': 'سيناريوهات معقدة، edge cases، وأفضل الممارسات الاحترافية',
}

TRACK_DIFFICULTY_GUIDANCE = {
    'frontend': {
        'beginner': 'أساسيات الوسوم والبنية في HTML/CSS/JS',
        'intermediate': 'سلوك المتصفح، النماذج، التخطيط، وDOM',
        'advanced': 'حالات متقدمة، أداء، إمكانية الوصول، وأنماط حديثة',
        'expert': 'سيناريوهات Frontend معقدة وأفضل الممارسات',
    },
    'python': {
        'beginner': 'أساسيات Python: أنواع البيانات، المتغيرات، والعمليات',
        'intermediate': 'دوال، شروط، حلقات، وتحويل الأنواع',
        'advanced': 'هياكل البيانات، list/dict/set، والخوارزميات البسيطة',
        'expert': 'OOP، الاستثناءات، context managers، وأنماط Pythonic',
    },
}


def is_ai_enabled() -> bool:
    return bool(getattr(settings, 'PLACEMENT_AI_ENABLED', False) and settings.GEMINI_API_KEY)


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)

    return json.loads(cleaned)


def _validate_question_payload(payload: dict, expected_topic: str, track_slug: str) -> dict:
    valid_topics = get_track_topics(track_slug)
    required_fields = ('question', 'options', 'correct_answer', 'explanation', 'topic', 'difficulty_level')
    for field in required_fields:
        if field not in payload:
            raise ValueError(f'Missing field: {field}')

    if payload['topic'] not in valid_topics:
        raise ValueError('Invalid topic')

    if payload['topic'] != expected_topic:
        payload['topic'] = expected_topic

    options = payload['options']
    if not isinstance(options, list) or len(options) != 4:
        raise ValueError('Options must contain exactly 4 items')

    options = [str(option).strip() for option in options]
    if len({option.lower() for option in options}) != 4:
        raise ValueError('Options must be unique')

    correct_answer = payload['correct_answer']
    if not isinstance(correct_answer, int) or correct_answer not in range(4):
        raise ValueError('correct_answer must be an integer from 0 to 3')

    difficulty_level = payload['difficulty_level']
    if difficulty_level not in DIFFICULTY_SCORES:
        raise ValueError('Invalid difficulty_level')

    question_text = str(payload['question']).strip()
    explanation = str(payload['explanation']).strip()
    if len(question_text) < 12 or len(explanation) < 8:
        raise ValueError('Question or explanation too short')

    return {
        'question': question_text,
        'options': options,
        'correct_answer': correct_answer,
        'explanation': explanation,
        'topic': payload['topic'],
        'difficulty_level': difficulty_level,
        'difficulty_score': DIFFICULTY_SCORES[difficulty_level],
    }


def _build_prompt(
    track_slug: str,
    topic: str,
    difficulty_level: str,
    exclude_questions: list[str],
    random_seed: int,
    step_index: int,
) -> str:
    track_config = get_track_config(track_slug)
    topic_label = track_config['topic_labels'][topic]
    guidance = TRACK_DIFFICULTY_GUIDANCE.get(track_slug, DIFFICULTY_GUIDANCE).get(
        difficulty_level,
        DIFFICULTY_GUIDANCE[difficulty_level],
    )
    excluded = '\n'.join(f'- {text}' for text in exclude_questions[:20]) or '- لا يوجد'
    return f"""أنت خبير تقييم {track_config['ai_domain']}. أنشئ سؤال اختيار من متعدد واحد باللغة العربية.

المتطلبات:
- المسار: {track_config['display_name']}
- الموضوع: {topic_label} ({topic})
- مستوى الصعوبة: {difficulty_level} — {guidance}
- 4 خيارات واقعية، واحد فقط صحيح
- السؤال يختبر فهماً حقيقياً وليس حفظاً سطحياً
- لا تكرر أي سؤال من القائمة أدناه
- استخدم seed={random_seed} وstep={step_index} لضمان تنوع السؤال

الأسئلة المستبعدة:
{excluded}

أعد JSON فقط بهذا الشكل:
{{
  "question": "نص السؤال",
  "options": ["الخيار 1", "الخيار 2", "الخيار 3", "الخيار 4"],
  "correct_answer": 0,
  "explanation": "شرح مختصر لماذا الإجابة صحيحة",
  "topic": "{topic}",
  "difficulty_level": "{difficulty_level}"
}}"""


def _call_gemini(prompt: str) -> str:
    api_key = settings.GEMINI_API_KEY
    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.95,
            'responseMimeType': 'application/json',
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.loads(response.read().decode('utf-8'))

    candidates = body.get('candidates') or []
    if not candidates:
        raise ValueError('Empty Gemini response')

    parts = candidates[0].get('content', {}).get('parts') or []
    if not parts:
        raise ValueError('Gemini response has no content')

    return parts[0].get('text', '')


def generate_question(
    track_slug: str,
    topic: str,
    ability_score: float,
    exclude_questions: list[str],
    random_seed: int,
    step_index: int,
) -> dict | None:
    if not is_ai_enabled():
        return None

    difficulty_level = ability_to_difficulty_level(ability_score)
    prompt = _build_prompt(
        track_slug,
        topic,
        difficulty_level,
        exclude_questions,
        random_seed,
        step_index,
    )

    for attempt in range(3):
        try:
            raw_text = _call_gemini(prompt)
            payload = _extract_json(raw_text)
            return _validate_question_payload(payload, topic, track_slug)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            logger.warning('AI question generation attempt %s failed: %s', attempt + 1, exc)

    return None


def save_generated_question(payload: dict, attempt, track_slug: str):
    from placement.models import PlacementQuestion

    return PlacementQuestion.objects.create(
        question=payload['question'],
        options=payload['options'],
        correct_answer=payload['correct_answer'],
        explanation=payload['explanation'],
        topic=payload['topic'],
        track_slug=track_slug,
        difficulty_level=payload['difficulty_level'],
        difficulty_score=payload['difficulty_score'],
        source='ai',
        attempt=attempt,
        is_active=True,
    )
