from uuid import uuid4

_MOCK_SESSION_DICT = {}

SESSION_OPEN = 'session-open'


def create_session():
    session_id = uuid4()
    new_session = {
        'id': session_id,
        'state': SESSION_OPEN,
    }
    _MOCK_SESSION_DICT[session_id] = new_session

    return new_session


def get_all_sessions():
    return list(_MOCK_SESSION_DICT.values())
