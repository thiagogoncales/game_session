import pytest

from session.models import Session


@pytest.yield_fixture(autouse=True)
def setup_dynamo():
    Session.create_table()
