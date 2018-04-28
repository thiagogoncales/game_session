import pytest

from game.models import Game
from session.models import Session


@pytest.yield_fixture(autouse=True)
def setup_dynamo():
    Game.create_table()
    Session.create_table()
