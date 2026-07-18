"""Helpers for WorkspaceBranch bootstrap and default workspace JSON."""

from __future__ import annotations

import json
import uuid

from django.db import IntegrityError, transaction

from .models import ProjectTask, TaskSubmission, WorkspaceBranch

FRONTEND_PROJECT_LANGUAGES = {
    'html',
    'css',
    'javascript',
    'typescript',
    'react',
}


def _file_id() -> str:
    return f'file-{uuid.uuid4().hex[:12]}'


def _starter_html(project_language: str) -> str:
    title = 'My React App' if project_language == 'react' else 'My Project'
    script_src = 'App.jsx' if project_language == 'react' else 'script.js'
    root = '  <div id="root"></div>\n' if project_language == 'react' else ''
    return (
        '<!DOCTYPE html>\n'
        '<html lang="ar">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <title>{title}</title>\n'
        '  <link rel="stylesheet" href="style.css">\n'
        '</head>\n'
        '<body>\n'
        f'{root}'
        f'  <script src="{script_src}"></script>\n'
        '</body>\n'
        '</html>\n'
    )


def _starter_react_component() -> str:
    return (
        'export default function App() {\n'
        '  return (\n'
        '    <div>\n'
        '      <h1>Hello React</h1>\n'
        '    </div>\n'
        '  )\n'
        '}\n'
    )


def get_default_file_name(project_language: str) -> str:
    return {
        'python': 'main.py',
        'html': 'index.html',
        'css': 'style.css',
        'javascript': 'script.js',
        'typescript': 'main.ts',
        'react': 'App.jsx',
        'java': 'Main.java',
    }.get(project_language, 'main.txt')


def get_default_workspace_json(project_language: str) -> str:
    """Mirror frontend getDefaultWorkspace for Main bootstrap when no submission exists."""
    if project_language in FRONTEND_PROJECT_LANGUAGES:
        html_id = _file_id()
        css_id = _file_id()
        js_id = _file_id()

        if project_language == 'react':
            files = [
                {'id': html_id, 'name': 'index.html', 'content': _starter_html('react')},
                {'id': css_id, 'name': 'style.css', 'content': ''},
                {'id': js_id, 'name': 'App.jsx', 'content': _starter_react_component()},
            ]
        else:
            files = [
                {
                    'id': html_id,
                    'name': 'index.html',
                    'content': _starter_html(project_language),
                },
                {'id': css_id, 'name': 'style.css', 'content': ''},
                {'id': js_id, 'name': 'script.js', 'content': ''},
            ]

        return json.dumps(
            {
                'version': 1,
                'activeFileId': html_id,
                'files': files,
            },
            ensure_ascii=False,
        )

    file_id = _file_id()
    return json.dumps(
        {
            'version': 1,
            'activeFileId': file_id,
            'files': [
                {
                    'id': file_id,
                    'name': get_default_file_name(project_language),
                    'content': '',
                }
            ],
        },
        ensure_ascii=False,
    )


def _primary_project_language(project) -> str:
    languages = project.get_languages_list()
    if languages:
        return languages[0]
    return project.language or 'python'


def _best_task_submission_answer(user, project) -> str:
    """Pick the richest TaskSubmission.answer among code tasks (legacy workspace)."""
    code_task_ids = ProjectTask.objects.filter(
        project=project,
        task_type='code',
    ).values_list('id', flat=True)

    submissions = TaskSubmission.objects.filter(
        user=user,
        project=project,
        task_id__in=code_task_ids,
    ).exclude(answer='')

    best_answer = ''
    best_score = -1

    for submission in submissions:
        answer = (submission.answer or '').strip()
        if not answer:
            continue

        score = len(answer)
        try:
            parsed = json.loads(answer)
            if isinstance(parsed, dict) and isinstance(parsed.get('files'), list):
                score = sum(len(str(f.get('content') or '')) for f in parsed['files'])
        except (TypeError, ValueError, json.JSONDecodeError):
            pass

        if score > best_score:
            best_score = score
            best_answer = submission.answer

    return best_answer or ''


def ensure_main_branch(user, project) -> WorkspaceBranch:
    """
    Ensure the user has a Main branch for this project.
    Initializes files_json from TaskSubmission.answer once, else default workspace.
    """
    existing = WorkspaceBranch.objects.filter(
        user=user,
        project=project,
        is_main=True,
    ).first()
    if existing:
        return existing

    files_json = _best_task_submission_answer(user, project)
    if not files_json.strip():
        files_json = get_default_workspace_json(_primary_project_language(project))

    try:
        with transaction.atomic():
            return WorkspaceBranch.objects.create(
                user=user,
                project=project,
                name='Main',
                files_json=files_json,
                is_main=True,
            )
    except IntegrityError:
        return WorkspaceBranch.objects.get(
            user=user,
            project=project,
            is_main=True,
        )
