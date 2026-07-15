from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max

from courses.models import Course
from projects.book_inventory_project import (
    BOOK_INVENTORY_PROJECT,
    BOOK_INVENTORY_TESTS,
    BOOK_INVENTORY_TITLE,
)
from projects.models import Project, ProjectTask, Tests
from projects.playing_cards_project import (
    PLAYING_CARDS_PROJECT,
    PLAYING_CARDS_TESTS,
    PLAYING_CARDS_TITLE,
)
from projects.product_catalog_project import (
    PRODUCT_CATALOG_PROJECT,
    PRODUCT_CATALOG_TESTS,
    PRODUCT_CATALOG_TITLE,
)
from projects.seed_data import FRONTEND_COURSE_TITLE
from projects.task_board_project import (
    TASK_BOARD_PROJECT,
    TASK_BOARD_TESTS,
    TASK_BOARD_TITLE,
)

LAB_PROJECTS = [
    (PLAYING_CARDS_TITLE, PLAYING_CARDS_PROJECT, PLAYING_CARDS_TESTS),
    (BOOK_INVENTORY_TITLE, BOOK_INVENTORY_PROJECT, BOOK_INVENTORY_TESTS),
    (TASK_BOARD_TITLE, TASK_BOARD_PROJECT, TASK_BOARD_TESTS),
    (PRODUCT_CATALOG_TITLE, PRODUCT_CATALOG_PROJECT, PRODUCT_CATALOG_TESTS),
]


class Command(BaseCommand):
    help = 'Create Frontend Mastery lab projects'

    @transaction.atomic
    def handle(self, *args, **options):
        course = Course.objects.filter(title=FRONTEND_COURSE_TITLE, is_active=True).first()
        if not course:
            self.stderr.write(
                self.style.ERROR(f'Course "{FRONTEND_COURSE_TITLE}" not found.')
            )
            return

        for title, project_data, tests in LAB_PROJECTS:
            project = self._upsert_project(course, project_data)
            self._seed_tasks_and_tests(project, project_data, tests)
            self.stdout.write(self.style.SUCCESS(
                f'Project "{title}" ready (id={project.id}) with '
                f'{len(project_data["stories"])} stories and {len(tests)} tests.'
            ))

        course.update_projects_count()
        self.stdout.write('Upload starter folders and images from the admin UI.')

    def _upsert_project(self, course, project_data):
        existing = Project.objects.filter(course=course, title=project_data['title']).first()

        if existing:
            project = existing
            project.description = project_data['description']
            project.level = project_data['level']
            project.languages = project_data['languages']
            project.language = project_data['languages'][0]
            project.objectives = project_data['objectives']
            project.estimated_time = project_data['estimated_time']
            project.is_active = True
            project.save()
            ProjectTask.objects.filter(project=project).delete()
            Tests.objects.filter(project=project).delete()
            self.stdout.write(f'Updating existing project id={project.id}')
            return project

        max_order = (
            Project.objects.filter(course=course).aggregate(Max('order'))['order__max'] or 0
        )
        project = Project.objects.create(
            course=course,
            title=project_data['title'],
            description=project_data['description'],
            level=project_data['level'],
            languages=project_data['languages'],
            language=project_data['languages'][0],
            objectives=project_data['objectives'],
            estimated_time=project_data['estimated_time'],
            order=max_order + 1,
            is_active=True,
        )
        self.stdout.write(f'Created project id={project.id}')
        return project

    def _seed_tasks_and_tests(self, project, project_data, tests):
        for index, story in enumerate(project_data['stories'], start=1):
            ProjectTask.objects.create(
                project=project,
                title=story['title'],
                description=story['description'],
                hint=story.get('hint', ''),
                task_type='code',
                order=index,
                expected_answer='',
                teaching='',
            )

        for test in tests:
            Tests.objects.create(
                project=project,
                name=test['name'],
                description=test['description'],
                test_code=test['test_code'],
                success_message=test['success_message'],
                failure_message=test['failure_message'],
            )
