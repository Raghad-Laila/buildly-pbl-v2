from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Max

from courses.models import Course
from projects.models import Project, ProjectTask, Tests
from projects.seed_data import FRONTEND_COURSE_TITLE
from projects.survey_form_project import (
    SURVEY_FORM_LEGACY_TITLES,
    SURVEY_FORM_PROJECT,
    SURVEY_FORM_TESTS,
    SURVEY_FORM_TITLE,
)


class Command(BaseCommand):
    help = 'Create the Arabic Survey Form lab project in Frontend Mastery'

    @transaction.atomic
    def handle(self, *args, **options):
        course = Course.objects.filter(title=FRONTEND_COURSE_TITLE, is_active=True).first()
        if not course:
            self.stderr.write(
                self.style.ERROR(f'Course "{FRONTEND_COURSE_TITLE}" not found.')
            )
            return

        lookup_titles = (SURVEY_FORM_TITLE, *SURVEY_FORM_LEGACY_TITLES)
        existing = Project.objects.filter(course=course, title__in=lookup_titles).first()
        if existing:
            project = existing
            self.stdout.write(f'Updating existing project id={project.id}')
            ProjectTask.objects.filter(project=project).delete()
            Tests.objects.filter(project=project).delete()
        else:
            max_order = (
                Project.objects.filter(course=course).aggregate(Max('order'))['order__max']
                or 0
            )
            project = Project.objects.create(
                course=course,
                title=SURVEY_FORM_PROJECT['title'],
                description=SURVEY_FORM_PROJECT['description'],
                level=SURVEY_FORM_PROJECT['level'],
                languages=SURVEY_FORM_PROJECT['languages'],
                language=SURVEY_FORM_PROJECT['languages'][0],
                objectives=SURVEY_FORM_PROJECT['objectives'],
                estimated_time=SURVEY_FORM_PROJECT['estimated_time'],
                order=max_order + 1,
                is_active=True,
            )
            self.stdout.write(f'Created project id={project.id}')

        if existing:
            project.title = SURVEY_FORM_PROJECT['title']
            project.description = SURVEY_FORM_PROJECT['description']
            project.level = SURVEY_FORM_PROJECT['level']
            project.languages = SURVEY_FORM_PROJECT['languages']
            project.language = SURVEY_FORM_PROJECT['languages'][0]
            project.objectives = SURVEY_FORM_PROJECT['objectives']
            project.estimated_time = SURVEY_FORM_PROJECT['estimated_time']
            project.is_active = True
            project.save()

        tasks_by_order = {}
        for index, story in enumerate(SURVEY_FORM_PROJECT['stories'], start=1):
            task = ProjectTask.objects.create(
                project=project,
                title=story['title'],
                description=story['description'],
                hint=story.get('hint', ''),
                task_type='code',
                order=index,
                expected_answer='',
                teaching='',
            )
            tasks_by_order[index] = task

        for test in SURVEY_FORM_TESTS:
            if 'story_index' not in test:
                raise CommandError(
                    f'Project "{SURVEY_FORM_TITLE}": test "{test.get("name", "<unknown>")}" '
                    f'is missing story_index.'
                )
            story_index = test['story_index']
            task = tasks_by_order.get(story_index)
            if task is None:
                raise CommandError(
                    f'Project "{SURVEY_FORM_TITLE}": test "{test.get("name", "<unknown>")}" '
                    f'has story_index={story_index} but no ProjectTask with that order exists.'
                )
            Tests.objects.create(
                project=project,
                task=task,
                name=test['name'],
                description=test['description'],
                test_code=test['test_code'],
                success_message=test['success_message'],
                failure_message=test['failure_message'],
            )

        course.update_projects_count()

        self.stdout.write(self.style.SUCCESS(
            f'Project "{SURVEY_FORM_TITLE}" ready in "{course.title}" '
            f'(id={project.id}) with {len(SURVEY_FORM_PROJECT["stories"])} stories '
            f'and {len(SURVEY_FORM_TESTS)} tests.'
        ))
        self.stdout.write(
            'Next: upload the starter folder and project image from the admin UI.'
        )
