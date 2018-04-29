import pytest

from game.models import Game
from participation.models import Participation
from session.models import Session


@pytest.yield_fixture(autouse=True)
def setup_dynamo():
    Game.create_table()
    Session.create_table()
    Participation.create_table()
