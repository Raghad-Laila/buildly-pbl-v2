from django.core.management.base import BaseCommand

from placement.models import PlacementQuestion
from placement.question_bank import PLACEMENT_QUESTIONS
from placement.python_question_bank import PYTHON_PLACEMENT_QUESTIONS


TRACK_QUESTIONS = {
    'frontend': PLACEMENT_QUESTIONS,
    'python': PYTHON_PLACEMENT_QUESTIONS,
}


class Command(BaseCommand):
    help = 'Seed adaptive placement question bank for Frontend and/or Python paths'

    def add_arguments(self, parser):
        parser.add_argument(
            '--track',
            choices=['frontend', 'python', 'all'],
            default='all',
            help='Which track question bank to seed',
        )

    def handle(self, *args, **options):
        track_option = options['track']
        tracks = ['frontend', 'python'] if track_option == 'all' else [track_option]
        created = 0
        updated = 0

        for track_slug in tracks:
            for item in TRACK_QUESTIONS[track_slug]:
                _, was_created = PlacementQuestion.objects.update_or_create(
                    question=item['question'],
                    topic=item['topic'],
                    difficulty_level=item['difficulty_level'],
                    track_slug=track_slug,
                    defaults={
                        'options': item['options'],
                        'correct_answer': item['correct_answer'],
                        'explanation': item['explanation'],
                        'difficulty_score': item['difficulty_score'],
                        'is_active': True,
                        'source': 'manual',
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        for track_slug in tracks:
            total = PlacementQuestion.objects.filter(is_active=True, track_slug=track_slug).count()
            self.stdout.write(
                self.style.SUCCESS(
                    f'{track_slug} placement questions ready: {total} active'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Seed complete ({created} created, {updated} updated)'
            )
        )
