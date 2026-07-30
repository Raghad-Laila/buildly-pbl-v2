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


def _normalize_text(text: str) -> str:
    cleaned = re.sub(r'\s+', ' ', str(text or '').strip().lower())
    cleaned = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', cleaned, flags=re.UNICODE)
    return re.sub(r'\s+', ' ', cleaned).strip()


def _significant_tokens(text: str) -> set[str]:
    stopwords = {
        'ال', 'و', 'في', 'من', 'على', 'إلى', 'عن', 'مع', 'هذا', 'هذه', 'ذلك', 'تلك',
        'ما', 'هو', 'هي', 'أو', 'لا', 'أن', 'إن', 'كان', 'يتم', 'يمكن', 'عند',
        'the', 'a', 'an', 'of', 'to', 'in', 'on', 'for', 'is', 'are', 'and', 'or',
        'what', 'which', 'who', 'how', 'does', 'do', 'did',
    }
    tokens = set()
    for token in _normalize_text(text).split(' '):
        if len(token) < 3:
            continue
        if token in stopwords:
            continue
        tokens.add(token)
    return tokens


def _similarity_ratio(left: str, right: str) -> float:
    left_tokens = _significant_tokens(left)
    right_tokens = _significant_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    overlap = len(left_tokens & right_tokens)
    return overlap / float(min(len(left_tokens), len(right_tokens)))


def _clip_option_text(option: str) -> str:
    return str(option or '').strip()


def _validate_question_payload(
    payload: dict,
    expected_topic: str,
    track_slug: str,
    *,
    expected_difficulty: str | None = None,
    exclude_questions: list[str] | None = None,
) -> dict:
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

    options = [_clip_option_text(option) for option in options]
    if any(not option for option in options):
        raise ValueError('Options must be non-empty')
    if any(len(option) > 140 for option in options):
        raise ValueError('Option text too long')
    if len({option.lower() for option in options}) != 4:
        raise ValueError('Options must be unique')

    correct_answer = payload['correct_answer']
    if isinstance(correct_answer, str) and correct_answer.strip().isdigit():
        correct_answer = int(correct_answer.strip())
    if not isinstance(correct_answer, int) or correct_answer not in range(4):
        raise ValueError('correct_answer must be an integer from 0 to 3')

    difficulty_level = payload['difficulty_level']
    if difficulty_level not in DIFFICULTY_SCORES:
        raise ValueError('Invalid difficulty_level')

    # Ability-driven difficulty is the source of truth for adaptive placement.
    if expected_difficulty:
        if expected_difficulty not in DIFFICULTY_SCORES:
            raise ValueError('Invalid expected difficulty')
        if difficulty_level != expected_difficulty:
            logger.info(
                'Placement AI difficulty mismatch (%s -> %s); coercing to ability target',
                difficulty_level,
                expected_difficulty,
            )
            difficulty_level = expected_difficulty

    question_text = str(payload['question']).strip()
    explanation = str(payload['explanation']).strip()
    if len(question_text) < 18:
        raise ValueError('Question too short')
    if len(question_text) > 320:
        raise ValueError('Question too long for timed placement')
    if len(explanation) < 12:
        raise ValueError('Explanation too short')
    if len(explanation) > 420:
        raise ValueError('Explanation too long')

    # Avoid options that merely copy the whole question stem.
    normalized_question = _normalize_text(question_text)
    for option in options:
        if _normalize_text(option) == normalized_question:
            raise ValueError('Option duplicates the question text')

    # Reject near-duplicates of recently asked questions (concept repetition).
    for previous in exclude_questions or []:
        if _similarity_ratio(question_text, previous) >= 0.72:
            raise ValueError('Question too similar to a previously asked question')

    # Soft topic relevance using topic label + common aliases.
    topic_label = get_track_config(track_slug)['topic_labels'].get(expected_topic, expected_topic)
    topic_aliases = {
        'html': ['html', 'htm', 'وسم', 'وسوم', 'عنصر', 'DOCTYPE', 'body', 'head', 'meta'],
        'css': ['css', 'ستايل', 'تنسيق', 'selector', 'خاصية', 'margin', 'padding', 'display'],
        'javascript': ['javascript', 'js', 'دالة', 'متغير', 'مصفوفة', 'object', 'event', 'dom'],
        'basics': ['python', 'بايثون', 'متغير', 'نوع', 'print', 'شرط', 'حلقة', 'أساسي'],
        'data_structures': ['list', 'dict', 'set', 'tuple', 'قائمة', 'قاموس', 'مجموعة', 'هيكل'],
        'oop': ['class', 'object', 'oop', 'كائن', 'صنف', 'وراثة', 'init', 'method'],
    }
    alias_tokens = set(topic_aliases.get(expected_topic, []))
    topic_tokens = _significant_tokens(f'{expected_topic} {topic_label}') | {
        token.lower() for token in alias_tokens
    }
    if topic_tokens:
        haystack = _normalize_text(' '.join([question_text, explanation, *options]))
        if not any(token in haystack for token in topic_tokens):
            raise ValueError('Question does not appear related to the target topic')

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
- الموضوع: {topic_label} ({topic}) — يجب أن يكون السؤال واضحاً عن هذا الموضوع فقط
- مستوى الصعوبة المطلوب بالضبط: {difficulty_level} — {guidance}
- difficulty_level في JSON يجب أن يساوي "{difficulty_level}" دون تغيير
- 4 خيارات واقعية ومختلفة الطول المعتدل، واحد فقط صحيح
- طول السؤال مناسب لاختبار زمني قصير (جملة إلى فقرة قصيرة)
- شرح مختصر واضح للإجابة الصحيحة
- السؤال يختبر فهماً حقيقياً وليس حفظاً سطحياً
- لا تكرر أي سؤال أو فكرة قريبة جداً من القائمة أدناه
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
            return _validate_question_payload(
                payload,
                topic,
                track_slug,
                expected_difficulty=difficulty_level,
                exclude_questions=exclude_questions,
            )
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
