"""Helpers prepended to Python project tests for flexible validation."""

PYTHON_TEST_HELPERS = '''
def resolve_fn(*names):
    for name in names:
        fn = globals().get(name)
        if callable(fn):
            return fn
    return None


def call_fn(names, *args):
    fn = resolve_fn(*names)
    if fn is None:
        raise AssertionError(f"function not found: {' | '.join(names)}")
    return fn(*args)


def assert_fn(names, args, expected):
    result = call_fn(names, *args)
    assert result == expected, f"expected {expected}, got {result}"


def assert_class_exists(*names):
    for name in names:
        cls = globals().get(name)
        if isinstance(cls, type):
            return cls
    raise AssertionError(f"class not found: {' | '.join(names)}")
'''.strip()


def wrap_python_test_code(student_code, test_code):
    return f'{student_code}\n\n{PYTHON_TEST_HELPERS}\n\n{test_code or ""}'.strip()
