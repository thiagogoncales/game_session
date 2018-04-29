from uuid import uuid4

from game.models import Game
from session.use_cases import get_active_session


def create_game(session_id, name, min_players, max_players):
    session = get_active_session(session_id=session_id)

    game_id = str(uuid4())
    new_game = Game(
        game_id=game_id,
        session_id=session_id,
        name=name,
        min_players=min_players,
        max_players=max_players,
    )
    new_game.save()

    return new_game.as_dict()


def get_game(session_id, game_id):
    try:
        return Game.get(session_id, game_id).as_dict()
    except Game.DoesNotExist:
        return None


def get_all_games_for_session(session_id):
    return [
        game.as_dict()
        for game in Game.query(session_id)
    ]
