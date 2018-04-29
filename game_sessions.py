from flask import (
    abort,
    Flask,
    jsonify,
    request,
)
from voluptuous import (
    All,
    Invalid,
    Length,
    MultipleInvalid,
    Range,
    Required,
    Schema,
)

from game.use_cases import (
    create_game,
    SessionClosedException,
)
from session.use_cases import (
    create_session,
    get_session,
    update_session,
)


app = Flask(__name__)


@app.route('/session/', methods=['POST'])
def session():
    return jsonify(create_session())


@app.route('/session/<session_id>/', methods=['GET', 'PUT'])
def session_detail(session_id):
    get_session_or_404(session_id)

    schema = Schema({
        Required('is_active'): bool,
    })

    if request.method == 'PUT':
        data = validate(request.get_json(), schema)
        return jsonify(update_session(session_id, **data))
    return jsonify(get_session(session_id))


@app.route('/session/<session_id>/game/', methods=['POST'])
def game(session_id):
    get_session_or_404(session_id)

    schema = Schema(All({
        Required('name'): All(str, Length(min=1)),
        Required('min_players'): All(int, Range(min=1)),
        Required('max_players'): All(int, Range(min=1)),
    }, min_players_must_be_less_than_max_players))

    data = validate(request.get_json(), schema)

    try:
        return jsonify(create_game(
            session_id=session_id,
            name=data['name'],
            min_players=data['min_players'],
            max_players=data['max_players'],
        ))
    except SessionClosedException:
        abort(403)


def min_players_must_be_less_than_max_players(data):
    if data['min_players'] >= data['max_players']:
        raise Invalid('min_players must be less than max_players')
    return data


def get_session_or_404(session_id):
    session = get_session(session_id)
    if not session:
        abort(404)
    return session


def validate(data, schema):
    try:
        return schema(request.get_json())
    except MultipleInvalid:
        abort(400)
