import random
from collections import Counter

from .constants import (
    ABILITY_STEP_CORRECT,
    ABILITY_STEP_WRONG,
    INITIAL_ABILITY_SCORE,
)
from .models import PlacementQuestion
from .services.question_generator import generate_question, is_ai_enabled, save_generated_question
from .track_config import get_track_for_attempt, get_track_topics


def get_topic_counts(asked_questions, topics) -> Counter:
    counts = Counter({topic: 0 for topic in topics})
    for question in asked_questions:
        counts[question.topic] += 1
    return counts


def get_topic_order(topics, random_seed: int) -> tuple:
    rng = random.Random(random_seed)
    topic_list = list(topics)
    rng.shuffle(topic_list)
    return tuple(topic_list)


def get_target_topic(topic_counts: Counter, topic_order: tuple, topics) -> str:
    for topic in topic_order:
        if topic_counts[topic] == 0:
            return topic

    return min(topics, key=lambda topic: topic_counts[topic])


def _question_sort_key(question, ability_score, topic_counts):
    return (
        abs(question.difficulty_score - ability_score),
        topic_counts[question.topic],
    )


def _pick_from_top_tier(candidates, ability_score, topic_counts, random_seed, step_index):
    candidates.sort(
        key=lambda question: _question_sort_key(question, ability_score, topic_counts)
        + (question.id,)
    )
    best_key = _question_sort_key(candidates[0], ability_score, topic_counts)
    top_tier = [
        question
        for question in candidates
        if _question_sort_key(question, ability_score, topic_counts) == best_key
    ]
    rng = random.Random(random_seed + step_index)
    return rng.choice(top_tier)


def _static_question_queryset(track_slug):
    return PlacementQuestion.objects.filter(
        is_active=True,
        source='manual',
        attempt__isnull=True,
        track_slug=track_slug,
    )


def _try_generate_ai_question(
    attempt,
    track_slug,
    preferred_topic,
    ability_score,
    asked_questions,
    random_seed,
    step_index,
):
    if not attempt or not is_ai_enabled():
        return None

    exclude_questions = [question.question for question in asked_questions]
    payload = generate_question(
        track_slug=track_slug,
        topic=preferred_topic,
        ability_score=ability_score,
        exclude_questions=exclude_questions,
        random_seed=random_seed,
        step_index=step_index,
    )
    if not payload:
        return None

    return save_generated_question(payload, attempt, track_slug)


def select_next_question(ability_score, used_ids, asked_questions, random_seed, attempt=None):
    track_slug = get_track_for_attempt(attempt) if attempt else None
    if not track_slug:
        return None

    topics = get_track_topics(track_slug)
    topic_counts = get_topic_counts(asked_questions, topics)
    topic_order = get_topic_order(topics, random_seed)
    preferred_topic = get_target_topic(topic_counts, topic_order, topics)
    step_index = len(asked_questions)

    if attempt:
        attempt_candidates = list(
            PlacementQuestion.objects.filter(
                is_active=True,
                attempt=attempt,
                track_slug=track_slug,
                topic=preferred_topic,
            ).exclude(id__in=used_ids)
        )
        if attempt_candidates:
            return _pick_from_top_tier(
                attempt_candidates, ability_score, topic_counts, random_seed, step_index
            )

        generated = _try_generate_ai_question(
            attempt,
            track_slug,
            preferred_topic,
            ability_score,
            asked_questions,
            random_seed,
            step_index,
        )
        if generated:
            return generated

    candidates = list(
        _static_question_queryset(track_slug).filter(topic=preferred_topic).exclude(id__in=used_ids)
    )

    if not candidates:
        candidates = list(_static_question_queryset(track_slug).exclude(id__in=used_ids))

    if not candidates:
        return None

    return _pick_from_top_tier(
        candidates, ability_score, topic_counts, random_seed, step_index
    )


def get_starting_question(random_seed, attempt=None):
    return select_next_question(INITIAL_ABILITY_SCORE, [], [], random_seed, attempt=attempt)


def apply_answer(ability_score: float, is_correct: bool) -> float:
    if is_correct:
        return round(ability_score + ABILITY_STEP_CORRECT, 2)
    return round(ability_score - ABILITY_STEP_WRONG, 2)
