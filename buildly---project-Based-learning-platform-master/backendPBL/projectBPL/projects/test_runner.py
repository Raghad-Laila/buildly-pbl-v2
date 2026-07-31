import os
import pathlib
import subprocess
import tempfile

from .test_helpers import wrap_python_test_code

ALLOWED_WORKSPACE_EXTENSIONS = {'.py', '.json', '.txt'}


def _safe_relative_path(file_name):
    """Return a path confined to the temp workspace, or None if unsafe."""
    cleaned = str(file_name or '').replace('\\', '/').lstrip('/')
    parts = [part for part in cleaned.split('/') if part and part not in ('.', '..')]
    if not parts:
        return None

    relative = '/'.join(parts)
    suffix = pathlib.Path(parts[-1]).suffix.lower()
    if suffix and suffix not in ALLOWED_WORKSPACE_EXTENSIONS:
        return None

    return relative


def _write_workspace_files(tmpdir, files, entry_file_name):
    written = []

    for item in files or []:
        if not isinstance(item, dict):
            continue

        relative = _safe_relative_path(item.get('name'))
        if not relative:
            continue

        absolute = os.path.join(tmpdir, *relative.split('/'))
        parent = os.path.dirname(absolute)
        if parent:
            os.makedirs(parent, exist_ok=True)

        content = item.get('content')
        if content is None:
            content = ''

        with open(absolute, 'w', encoding='utf-8') as handle:
            handle.write(str(content))

        written.append(relative)

    if not written:
        raise ValueError('No safe workspace files provided for Docker execution')

    entry = _safe_relative_path(entry_file_name) or 'main.py'
    if entry not in written:
        raise ValueError(f'Entry file "{entry_file_name}" was not found in workspace files')

    return entry


def run_python_in_docker(code=None, timeout=30, files=None, entry_file_name='main.py'):
    """
    Run Python in Docker.

    Legacy:
        run_python_in_docker(code_string)

    Multi-file:
        run_python_in_docker(files=[...], entry_file_name='main.py')

    timeout covers container startup + code. Docker Desktop on Windows often
    needs well above a few seconds just to start --rm containers.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        if files is not None:
            entry = _write_workspace_files(tmpdir, files, entry_file_name)
        else:
            if code is None:
                raise ValueError('Either code or files must be provided')

            entry = 'main.py'
            file_path = os.path.join(tmpdir, entry)
            with open(file_path, 'w', encoding='utf-8') as handle:
                handle.write(code)

        tmpdir_path = pathlib.Path(tmpdir).resolve()
        docker_path = tmpdir_path.as_posix()

        result = subprocess.run(
            [
                'docker',
                'run',
                '--rm',
                '-v',
                f'{docker_path}:/app',
                '--network',
                'none',
                '--memory',
                '100m',
                '--cpus',
                '0.5',
                'python-runner-image',
                'python3',
                entry,
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
        }


def _normalize_workspace_files(files):
    prepared = []
    for item in files or []:
        if not isinstance(item, dict):
            continue
        relative = _safe_relative_path(item.get('name'))
        if not relative:
            continue
        content = item.get('content')
        if content is None:
            content = ''
        prepared.append({'name': relative, 'content': str(content)})
    return prepared


def _files_with_wrapped_entry(files, entry_file_name, test_code):
    """Copy workspace files and append helpers + test code to the entry file."""
    prepared = _normalize_workspace_files(files)
    entry = _safe_relative_path(entry_file_name) or 'main.py'

    if not prepared:
        raise ValueError('No safe workspace files provided for Docker execution')

    found = False
    wrapped = []
    for item in prepared:
        content = item['content']
        if item['name'] == entry:
            content = wrap_python_test_code(content, test_code)
            found = True
        wrapped.append({'name': item['name'], 'content': content})

    if not found:
        raise ValueError(f'Entry file "{entry_file_name}" was not found in workspace files')

    return wrapped, entry


def _run_single_python_test(code, test_code, files=None, entry_file_name='main.py'):
    if files is not None:
        wrapped_files, entry = _files_with_wrapped_entry(files, entry_file_name, test_code)
        return run_python_in_docker(
            files=wrapped_files,
            entry_file_name=entry,
        )

    combined_code = wrap_python_test_code(code or '', test_code)
    return run_python_in_docker(combined_code)


def run_project_tests(code, language, tests_queryset, files=None, entry_file_name='main.py'):
    results = []
    has_files = isinstance(files, list) and len(files) > 0
    workspace_files = files if has_files else None

    for test in tests_queryset:
        if language != 'python':
            results.append(
                {
                    'id': test.id,
                    'name': test.name,
                    'passed': False,
                    'message': (
                        test.failure_message
                        or f"تشغيل الاختبارات على السيرفر غير مدعوم حالياً للغة '{language}'."
                    ),
                    'error': '',
                    'stdout': '',
                    'stderr': '',
                }
            )
            continue

        try:
            outcome = _run_single_python_test(
                code,
                test.test_code or '',
                files=workspace_files,
                entry_file_name=entry_file_name or 'main.py',
            )
            stderr = (outcome.get('stderr') or '').strip()
            # Assertions fail with non-zero returncode. Do not treat stderr-only
            # warnings as failure when the process exits successfully.
            passed = outcome.get('returncode') == 0

            if passed:
                message = test.success_message or 'نجح الاختبار'
                error = ''
            else:
                error = stderr
                message = test.failure_message or (stderr if stderr else 'فشل الاختبار')

            results.append(
                {
                    'id': test.id,
                    'name': test.name,
                    'passed': passed,
                    'message': message,
                    'error': error,
                    'stdout': outcome.get('stdout') or '',
                    'stderr': stderr,
                }
            )
        except subprocess.TimeoutExpired:
            results.append(
                {
                    'id': test.id,
                    'name': test.name,
                    'passed': False,
                    'message': test.failure_message or 'انتهت مهلة تنفيذ الاختبار',
                    'error': 'Execution timeout',
                    'stdout': '',
                    'stderr': 'Execution timeout',
                }
            )
        except Exception as exc:
            error_text = str(exc)
            results.append(
                {
                    'id': test.id,
                    'name': test.name,
                    'passed': False,
                    'message': test.failure_message or error_text,
                    'error': error_text,
                    'stdout': '',
                    'stderr': error_text,
                }
            )

    passed_count = sum(1 for item in results if item['passed'])

    return {
        'results': results,
        'summary': {
            'total': len(results),
            'passed': passed_count,
            'failed': len(results) - passed_count,
        },
    }
