import pytest


@pytest.fixture(scope="session")
def pub_data():
    data = {'token':'asdfasdfjsldkfjlsxllkj'}
    return data