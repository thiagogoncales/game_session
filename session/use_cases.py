from uuid import uuid4

from session.models import Session
from session.game_session import get_game_sessions


class SessionClosedException(Exception):
    pass


class SessionOpenException(Exception):
    pass


def create_session(is_active=True):
    session_id = str(uuid4())

    new_session = Session(
        session_id=session_id,
        is_active=is_active,
    )
    new_session.save()

    return new_session.as_dict()


def get_session(session_id):
    try:
        return _get_session(session_id).as_dict()
    except Session.DoesNotExist:
        return None

def get_active_session(session_id):
    session = get_session(session_id)
    if not session:
        return session

    if not session['is_active']:
        raise SessionClosedException


def update_session(session_id, **kwargs):
    session = Session(
        session_id=session_id,
        **kwargs
    )
    session.save()
    return session.as_dict()


def set_game_session_active_status(session_id, is_active):
    session = _get_session(session_id)
    session.update(actions=[
        Session.is_active.set(is_active),
    ])
    return session.as_dict()


def get_game_session(session_id):
    from game.use_cases import get_all_games_for_session
    from participation.use_cases import get_all_participation_for_session

    session = get_session(session_id)
    if not session:
        return session

    if session['is_active']:
        raise SessionOpenException

    games_in_session = get_all_games_for_session(session_id)
    participation_in_session = get_all_participation_for_session(session_id)

    return {
        'session_id': session_id,
        'game_sessions': get_game_sessions(
            games_in_session,
            participation_in_session,
        ),
    }

def _get_session(session_id):
    return Session.get(session_id)
