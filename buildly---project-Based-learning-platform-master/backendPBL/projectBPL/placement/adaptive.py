from collections import Counter

from .constants import (
    ABILITY_STEP_CORRECT,
    ABILITY_STEP_WRONG,
    INITIAL_ABILITY_SCORE,
    TOPICS,
    TOTAL_QUESTIONS,
)
from .models import PlacementQuestion


def get_topic_counts(asked_questions) -> Counter:
    counts = Counter({topic: 0 for topic in TOPICS})
    for question in asked_questions:
        counts[question.topic] += 1
    return counts


def get_target_topic(topic_counts: Counter, questions_answered: int) -> str:
    for topic in TOPICS:
        if topic_counts[topic] == 0:
            return topic

    return min(TOPICS, key=lambda topic: topic_counts[topic])


def select_next_question(ability_score, used_ids, asked_questions):
    topic_counts = get_topic_counts(asked_questions)
    preferred_topic = get_target_topic(topic_counts, len(asked_questions))

    candidates = list(
        PlacementQuestion.objects.filter(is_active=True, topic=preferred_topic).exclude(
            id__in=used_ids
        )
    )

    if not candidates:
        candidates = list(
            PlacementQuestion.objects.filter(is_active=True).exclude(id__in=used_ids)
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda question: (
            abs(question.difficulty_score - ability_score),
            topic_counts[question.topic],
            question.id,
        )
    )
    return candidates[0]


def get_starting_question():
    return select_next_question(INITIAL_ABILITY_SCORE, [], [])


def apply_answer(ability_score: float, is_correct: bool) -> float:
    if is_correct:
        return round(ability_score + ABILITY_STEP_CORRECT, 2)
    return round(ability_score - ABILITY_STEP_WRONG, 2)
