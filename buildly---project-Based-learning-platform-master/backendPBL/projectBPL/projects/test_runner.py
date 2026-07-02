import os
import pathlib
import subprocess
import tempfile


def run_python_in_docker(code, timeout=5):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'main.py')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(code)

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


def run_project_tests(code, language, tests_queryset):
    results = []

    for test in tests_queryset:
        combined_code = f'{code}\n\n{test.test_code or ""}'.strip()

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
            outcome = run_python_in_docker(combined_code)
            stderr = (outcome.get('stderr') or '').strip()
            passed = outcome.get('returncode') == 0 and not stderr

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
