from django.core.management.base import BaseCommand
from django.db import transaction

from account.models import CustomUser
from courses.models import Course
from projects.models import Project, ProjectTask, Tests
from projects.seed_data import (
    FRONTEND_COURSE_TITLE,
    FRONTEND_PROJECTS,
    PYTHON_COURSE_TITLE,
    PYTHON_COURSE_FALLBACK_TITLE,
    PYTHON_PROJECTS,
    SEED_PREFIX,
)


class Command(BaseCommand):
    help = 'Seed demo projects for Frontend and Python learning paths'

    def add_arguments(self, parser):
        parser.add_argument(
            '--deactivate-old',
            action='store_true',
            help='Deactivate old projects in target courses that are not Buildly seeds',
        )
        parser.add_argument(
            '--python-only',
            action='store_true',
            help='Seed Python course projects only',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        admin = (
            CustomUser.objects.filter(user_type='admin', is_active=True).first()
            or CustomUser.objects.filter(user_type='مشرف', is_active=True).first()
        )

        if not admin:
            self.stderr.write(self.style.ERROR('No admin user found.'))
            return

        python_course = self._ensure_python_course(admin)

        if options['deactivate_old']:
            self._deactivate_old_projects(python_course)

        python_count = self._seed_projects(python_course, PYTHON_PROJECTS)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {python_count} python projects in "{python_course.title}" '
            f'(id={python_course.id})'
        ))

        if options['python_only']:
            self.stdout.write(self.style.SUCCESS(
                f'Admin: {admin.email} | Look for projects starting with "{SEED_PREFIX}"'
            ))
            return

        frontend_course = self._get_frontend_course()

        if options['deactivate_old']:
            self._deactivate_old_projects(frontend_course)

        frontend_count = self._seed_projects(frontend_course, FRONTEND_PROJECTS)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {frontend_count} frontend projects in "{frontend_course.title}" '
            f'(id={frontend_course.id})'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Admin: {admin.email} | Look for projects starting with "{SEED_PREFIX}"'
        ))

    def _get_frontend_course(self):
        course = Course.objects.filter(title=FRONTEND_COURSE_TITLE, is_active=True).first()
        if course:
            return course

        raise ValueError(
            f'Frontend course "{FRONTEND_COURSE_TITLE}" not found. Create it first or update seed_data.'
        )

    def _ensure_python_course(self, admin):
        course = (
            Course.objects.filter(title=PYTHON_COURSE_TITLE, is_active=True).first()
            or Course.objects.filter(title=PYTHON_COURSE_TITLE).first()
            or Course.objects.filter(title=PYTHON_COURSE_FALLBACK_TITLE).first()
        )

        if course:
            changed = False
            if not course.is_active:
                course.is_active = True
                changed = True
            if course.is_archived:
                course.is_archived = False
                changed = True
            if not course.is_public:
                course.is_public = True
                changed = True
            if changed:
                course.save()
            return course

        return Course.objects.create(
            title=PYTHON_COURSE_TITLE,
            description=(
                'مسار شامل لتعلم Python من الصفر حتى المستوى الخبير. '
                'يتضمن مشاريع عملية مع اختبارات آلية لكل مرحلة.'
            ),
            level='beginner',
            category='language',
            estimated_duration=40,
            is_public=True,
            is_active=True,
            instructor=admin,
        )

    def _deactivate_old_projects(self, course):
        updated = Project.objects.filter(
            course=course,
            is_active=True,
        ).exclude(
            title__startswith=SEED_PREFIX,
        ).update(is_active=False)

        if updated:
            course.update_projects_count()

        self.stdout.write(f'Deactivated {updated} old projects in "{course.title}"')

    def _seed_projects(self, course, project_defs):
        seeded = 0

        for order, data in enumerate(project_defs, start=1):
            project, _ = Project.objects.update_or_create(
                course=course,
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'level': data['level'],
                    'languages': data['languages'],
                    'language': data['languages'][0],
                    'objectives': '\n'.join(data['objectives']),
                    'estimated_time': data['estimated_time'],
                    'order': order,
                    'is_active': True,
                    'assets_provided': data.get('assets_provided', []),
                    'ideas_to_test': data.get('ideas_to_test', []),
                },
            )

            ProjectTask.objects.filter(project=project).delete()
            Tests.objects.filter(project=project).delete()

            for index, story in enumerate(data['stories'], start=1):
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

            for test in data['tests']:
                Tests.objects.create(
                    project=project,
                    name=test['name'],
                    description=test['description'],
                    test_code=test['test_code'],
                    success_message=test['success_message'],
                    failure_message=test['failure_message'],
                )

            seeded += 1

        course.update_projects_count()
        return seeded
