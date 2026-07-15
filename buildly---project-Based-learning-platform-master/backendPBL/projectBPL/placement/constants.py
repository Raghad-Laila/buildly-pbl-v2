from .track_config import ALL_TOPICS, FRONTEND_COURSE_TITLE, requires_placement_course

TOTAL_QUESTIONS = 12
QUESTION_TIME_LIMIT_SECONDS = 20

INITIAL_ABILITY_SCORE = 0.0

ABILITY_STEP_CORRECT = 0.4
ABILITY_STEP_WRONG = 0.4

TOPICS = ALL_TOPICS

DIFFICULTY_LEVELS = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
)

DIFFICULTY_SCORES = {
    'beginner': -1.0,
    'intermediate': 0.0,
    'advanced': 1.0,
    'expert': 2.0,
}

FINAL_LEVELS = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
)


def ability_to_final_level(ability_score: float) -> str:
    if ability_score < -0.6:
        return 'beginner'
    if ability_score < 0.2:
        return 'intermediate'
    if ability_score < 0.8:
        return 'advanced'
    return 'expert'


def ability_to_difficulty_level(ability_score: float) -> str:
    if ability_score < -0.5:
        return 'beginner'
    if ability_score < 0.3:
        return 'intermediate'
    if ability_score < 1.0:
        return 'advanced'
    return 'expert'


def is_frontend_placement_course(course) -> bool:
    """Legacy helper kept for backward compatibility."""
    from .track_config import get_track_for_course

    return get_track_for_course(course) == 'frontend'


__all__ = [
    'FRONTEND_COURSE_TITLE',
    'TOTAL_QUESTIONS',
    'INITIAL_ABILITY_SCORE',
    'ABILITY_STEP_CORRECT',
    'ABILITY_STEP_WRONG',
    'TOPICS',
    'DIFFICULTY_LEVELS',
    'DIFFICULTY_SCORES',
    'FINAL_LEVELS',
    'ability_to_final_level',
    'ability_to_difficulty_level',
    'is_frontend_placement_course',
    'requires_placement_course',
]
