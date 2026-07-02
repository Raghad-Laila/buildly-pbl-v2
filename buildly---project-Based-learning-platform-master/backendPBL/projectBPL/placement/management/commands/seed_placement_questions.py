from django.core.management.base import BaseCommand

from placement.models import PlacementQuestion
from placement.question_bank import PLACEMENT_QUESTIONS


class Command(BaseCommand):
    help = 'Seed adaptive placement question bank for Frontend path'

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for item in PLACEMENT_QUESTIONS:
            question, was_created = PlacementQuestion.objects.update_or_create(
                question=item['question'],
                topic=item['topic'],
                difficulty_level=item['difficulty_level'],
                defaults={
                    'options': item['options'],
                    'correct_answer': item['correct_answer'],
                    'explanation': item['explanation'],
                    'difficulty_score': item['difficulty_score'],
                    'is_active': True,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        total = PlacementQuestion.objects.filter(is_active=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Placement questions ready: {total} active ({created} created, {updated} updated)'
            )
        )
