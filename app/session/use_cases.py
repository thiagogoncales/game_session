from uuid import uuid4

from session.constants import SESSION_OPEN

_MOCK_SESSION_DICT = {}


def create_session():
    session_id = str(uuid4())
    new_session = {
        'id': session_id,
        'state': SESSION_OPEN,
    }
    _MOCK_SESSION_DICT[session_id] = new_session

    return new_session


def get_all_sessions():
    return list(_MOCK_SESSION_DICT.values())

def get_session(session_id):
    return _MOCK_SESSION_DICT[session_id]
