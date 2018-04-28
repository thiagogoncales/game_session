from uuid import uuid4

from session.models import Session


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
