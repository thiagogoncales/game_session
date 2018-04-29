from participation.models import Participation
from session.use_cases import get_active_session


def add_participation(session_id, user_id, name, preferences):
    get_active_session(session_id=session_id)

    new_participation = Participation(
        session_id=session_id,
        user_id=user_id,
        name=name,
        preferences=preferences,
    )
    new_participation.save()

    return new_participation.as_dict()


def get_participation(session_id, user_id):
    try:
        return Participation.get(session_id, user_id).as_dict()
    except Participation.DoesNotExist:
        return None


def get_all_participation_for_session(session_id):
    return [
        participation.as_dict()
        for participation in Participation.query(session_id)
    ]
