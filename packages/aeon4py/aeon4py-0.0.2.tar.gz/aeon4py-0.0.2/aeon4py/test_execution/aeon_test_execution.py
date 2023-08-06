from aeon4py import get_adapter


def before_start(suite_name: str, working_directory=None):
    get_adapter(working_directory=working_directory).before_start(suite_name)


def done():
    get_adapter().done()


def given(message: str):
    get_adapter().given(message)


def and_given(message: str):
    get_adapter().and_given(message)


def when(message: str):
    get_adapter().when(message)


def and_when(message: str):
    get_adapter().and_when(message)


def then(message: str):
    get_adapter().then(message)


def and_then(message: str):
    get_adapter().and_then(message)


def start_test(name: str):
    get_adapter().start_test(name)


def test_succeeded():
    get_adapter().test_succeeded()


def test_failed(message: str, exception=None):
    get_adapter().test_failed(message, exception)