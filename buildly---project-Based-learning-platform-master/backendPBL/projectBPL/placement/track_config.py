FRONTEND_COURSE_TITLE = 'Frontend Mastery'
PYTHON_COURSE_TITLE = 'Python'
PYTHON_COURSE_FALLBACK_TITLE = 'مسار تعلم Python'

PLACEMENT_TRACKS = {
    'frontend': {
        'course_titles': [FRONTEND_COURSE_TITLE],
        'topics': ('html', 'css', 'javascript'),
        'topic_labels': {
            'html': 'HTML',
            'css': 'CSS',
            'javascript': 'JavaScript',
        },
        'display_name': 'Frontend',
        'skills_description': 'HTML · CSS · JavaScript',
        'join_note': 'سيبدأ اختبار تحديد مستوى Frontend قبل الانضمام للمسار.',
        'ai_domain': 'Frontend (HTML, CSS, JavaScript)',
    },
    'python': {
        'course_titles': [PYTHON_COURSE_TITLE, PYTHON_COURSE_FALLBACK_TITLE],
        'topics': ('basics', 'data_structures', 'oop'),
        'topic_labels': {
            'basics': 'أساسيات Python',
            'data_structures': 'هياكل البيانات',
            'oop': 'OOP',
        },
        'display_name': 'Python',
        'skills_description': 'أساسيات Python · هياكل البيانات · OOP',
        'join_note': 'سيبدأ اختبار تحديد مستوى Python قبل الانضمام للمسار.',
        'ai_domain': 'Python (basics, data structures, OOP)',
    },
}

ALL_TOPICS = tuple(
    topic
    for track in PLACEMENT_TRACKS.values()
    for topic in track['topics']
)


def _normalize_title(title: str) -> str:
    return title.strip().lower()


def get_track_for_course(course) -> str | None:
    title = _normalize_title(course.title)
    for track_slug, config in PLACEMENT_TRACKS.items():
        for course_title in config['course_titles']:
            if title == _normalize_title(course_title):
                return track_slug
    return None


def requires_placement_course(course) -> bool:
    return get_track_for_course(course) is not None


def get_track_config(track_slug: str) -> dict:
    return PLACEMENT_TRACKS[track_slug]


def get_track_topics(track_slug: str) -> tuple:
    return get_track_config(track_slug)['topics']


def get_track_topic_labels(track_slug: str) -> dict:
    return get_track_config(track_slug)['topic_labels']


def get_track_for_attempt(attempt) -> str | None:
    return get_track_for_course(attempt.course)


def build_track_status_meta(course) -> dict:
    track_slug = get_track_for_course(course)
    if not track_slug:
        return {
            'track_slug': None,
            'track_display_name': None,
            'topics': [],
            'topic_labels': {},
            'skills_description': None,
        }

    config = get_track_config(track_slug)
    return {
        'track_slug': track_slug,
        'track_display_name': config['display_name'],
        'topics': list(config['topics']),
        'topic_labels': config['topic_labels'],
        'skills_description': config['skills_description'],
    }
