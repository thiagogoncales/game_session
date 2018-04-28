import pytest

import game_sessions
from session.use_cases import (
    create_session,
)


@pytest.fixture
def client():
    return game_sessions.app.test_client()


@pytest.fixture
def active_session():
    return create_session(is_active=True)

@pytest.fixture
def inactive_session():
    return create_session(is_active=False)
