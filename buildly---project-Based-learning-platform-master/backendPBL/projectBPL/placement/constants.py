FRONTEND_COURSE_TITLE = 'Frontend Mastery'

TOTAL_QUESTIONS = 12

INITIAL_ABILITY_SCORE = 0.0

ABILITY_STEP_CORRECT = 0.4
ABILITY_STEP_WRONG = 0.4

TOPICS = ('html', 'css', 'javascript')

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


def is_frontend_placement_course(course) -> bool:
    return course.title.strip().lower() == FRONTEND_COURSE_TITLE.lower()
