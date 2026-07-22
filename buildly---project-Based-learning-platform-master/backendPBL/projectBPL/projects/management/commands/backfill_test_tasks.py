from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from projects.book_inventory_project import BOOK_INVENTORY_TESTS, BOOK_INVENTORY_TITLE
from projects.models import Project, ProjectTask, Tests
from projects.playing_cards_project import PLAYING_CARDS_TESTS, PLAYING_CARDS_TITLE
from projects.product_catalog_project import PRODUCT_CATALOG_TESTS, PRODUCT_CATALOG_TITLE
from projects.seed_data import FRONTEND_PROJECTS, PYTHON_PROJECTS
from projects.survey_form_project import SURVEY_FORM_TESTS, SURVEY_FORM_TITLE
from projects.task_board_project import TASK_BOARD_TESTS, TASK_BOARD_TITLE

LAB_DEFINITIONS = {
    PLAYING_CARDS_TITLE: PLAYING_CARDS_TESTS,
    BOOK_INVENTORY_TITLE: BOOK_INVENTORY_TESTS,
    TASK_BOARD_TITLE: TASK_BOARD_TESTS,
    PRODUCT_CATALOG_TITLE: PRODUCT_CATALOG_TESTS,
    SURVEY_FORM_TITLE: SURVEY_FORM_TESTS,
}

DEMO_DEFINITIONS = {
    project['title']: project
    for project in (*FRONTEND_PROJECTS, *PYTHON_PROJECTS)
}


class Command(BaseCommand):
    help = (
        'Backfill Tests.task for known lab projects (story_index) and '
        'demo projects (positional 1:1 seed mapping).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report planned links without writing to the database.',
        )
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Persist Tests.task links inside a transaction.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        apply = options['apply']

        if dry_run == apply:
            raise CommandError('Specify exactly one of --dry-run or --apply.')

        if apply:
            with transaction.atomic():
                summary = self._backfill(persist=True)
        else:
            summary = self._backfill(persist=False)

        self._print_summary(summary, dry_run=dry_run)

    def _backfill(self, persist):
        summary = {
            'lab_linked': 0,
            'demo_linked': 0,
            'skipped_already_linked': 0,
            'skipped_ambiguous_projects': [],
            'unresolved_tests': [],
            'missing_story_task_mappings': [],
        }

        self._backfill_labs(persist, summary)
        self._backfill_demos(persist, summary)
        return summary

    def _backfill_labs(self, persist, summary):
        for title, test_defs in LAB_DEFINITIONS.items():
            projects = Project.objects.filter(title=title)
            if not projects.exists():
                continue

            defs_by_name = {tdef['name']: tdef for tdef in test_defs}

            for project in projects:
                tasks_by_order = {
                    task.order: task
                    for task in ProjectTask.objects.filter(project=project)
                }

                tests = Tests.objects.filter(project=project).order_by('id')
                for test in tests:
                    if test.task_id is not None:
                        summary['skipped_already_linked'] += 1
                        continue

                    tdef = defs_by_name.get(test.name)
                    if tdef is None:
                        summary['unresolved_tests'].append(
                            f'project_id={project.id} test_id={test.id} '
                            f'name={test.name!r} (no matching lab definition name)'
                        )
                        continue

                    if 'story_index' not in tdef:
                        summary['missing_story_task_mappings'].append(
                            f'project_id={project.id} test_id={test.id} '
                            f'name={test.name!r} (definition missing story_index)'
                        )
                        continue

                    story_index = tdef['story_index']
                    task = tasks_by_order.get(story_index)
                    if task is None:
                        summary['missing_story_task_mappings'].append(
                            f'project_id={project.id} test_id={test.id} '
                            f'name={test.name!r} story_index={story_index} '
                            f'(no ProjectTask with that order)'
                        )
                        continue

                    if task.project_id != test.project_id:
                        summary['missing_story_task_mappings'].append(
                            f'project_id={project.id} test_id={test.id} '
                            f'name={test.name!r} (cross-project task rejected)'
                        )
                        continue

                    if persist:
                        updated = Tests.objects.filter(
                            pk=test.pk,
                            task__isnull=True,
                        ).update(task=task)
                        if updated != 1:
                            summary['skipped_already_linked'] += 1
                            continue

                    summary['lab_linked'] += 1

    def _backfill_demos(self, persist, summary):
        for title, demo_def in DEMO_DEFINITIONS.items():
            projects = Project.objects.filter(title=title)
            if not projects.exists():
                continue

            seed_names = [tdef['name'] for tdef in demo_def['tests']]

            for project in projects:
                tasks = list(
                    ProjectTask.objects.filter(project=project).order_by('order')
                )
                tests = list(
                    Tests.objects.filter(project=project).order_by('id')
                )

                if len(tasks) != len(tests):
                    summary['skipped_ambiguous_projects'].append(
                        f'project_id={project.id} title={title!r} '
                        f'(tasks={len(tasks)} tests={len(tests)}; counts differ)'
                    )
                    continue

                if len(tests) != len(seed_names):
                    summary['skipped_ambiguous_projects'].append(
                        f'project_id={project.id} title={title!r} '
                        f'(db tests={len(tests)} seed tests={len(seed_names)}; '
                        f'counts differ)'
                    )
                    continue

                db_names = [test.name for test in tests]
                if db_names != seed_names:
                    summary['skipped_ambiguous_projects'].append(
                        f'project_id={project.id} title={title!r} '
                        f'(test names do not match seed order)'
                    )
                    continue

                tasks_by_order = {task.order: task for task in tasks}
                planned = []
                ambiguous = False

                for index, test in enumerate(tests):
                    if test.task_id is not None:
                        summary['skipped_already_linked'] += 1
                        continue

                    story_index = index + 1
                    task = tasks_by_order.get(story_index)
                    if task is None or task.project_id != test.project_id:
                        summary['skipped_ambiguous_projects'].append(
                            f'project_id={project.id} title={title!r} '
                            f'(cannot resolve task order={story_index} for '
                            f'test_id={test.id})'
                        )
                        ambiguous = True
                        break

                    planned.append((test, task))

                if ambiguous:
                    continue

                for test, task in planned:
                    if persist:
                        updated = Tests.objects.filter(
                            pk=test.pk,
                            task__isnull=True,
                        ).update(task=task)
                        if updated != 1:
                            summary['skipped_already_linked'] += 1
                            continue

                    summary['demo_linked'] += 1

    def _print_summary(self, summary, dry_run):
        mode = 'DRY-RUN' if dry_run else 'APPLY'
        self.stdout.write(self.style.SUCCESS(f'[{mode}] backfill_test_tasks complete'))
        self.stdout.write(f'lab links: {summary["lab_linked"]}')
        self.stdout.write(f'demo links: {summary["demo_linked"]}')
        self.stdout.write(
            f'skipped already linked: {summary["skipped_already_linked"]}'
        )
        self.stdout.write(
            f'skipped ambiguous projects: {len(summary["skipped_ambiguous_projects"])}'
        )
        for item in summary['skipped_ambiguous_projects']:
            self.stdout.write(f'  - {item}')
        self.stdout.write(f'unresolved tests: {len(summary["unresolved_tests"])}')
        for item in summary['unresolved_tests']:
            self.stdout.write(f'  - {item}')
        self.stdout.write(
            f'missing story/task mappings: {len(summary["missing_story_task_mappings"])}'
        )
        for item in summary['missing_story_task_mappings']:
            self.stdout.write(f'  - {item}')
