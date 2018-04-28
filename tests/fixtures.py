import pytest

import game_sessions


@pytest.fixture
def client():
    return game_sessions.app.test_client()
