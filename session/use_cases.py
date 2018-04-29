from uuid import uuid4

from session.models import Session


class SessionClosedException(Exception):
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
        return Session.get(session_id).as_dict()
    except Session.DoesNotExist:
        return None

def get_active_session(session_id):
    session = get_session(session_id)
    if not session:
        return session

    if not session['is_active']:
        raise SessionClosedException


def update_session(session_id, **kwargs):
    print(kwargs)
    session = Session(
        session_id=session_id,
        **kwargs
    )
    session.save()
    return session.as_dict()
