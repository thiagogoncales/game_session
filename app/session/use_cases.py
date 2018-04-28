from uuid import uuid4

from session.constants import SESSION_OPEN
from session.models import Session


def create_session():
    session_id = str(uuid4())

    new_session = Session(
        session_id=session_id,
        is_active=True,
    )
    new_session.save()

    return new_session.as_dict()


def get_session(session_id):
    return Session.get(session_id).as_dict()
