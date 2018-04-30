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

from game.schemas import game_schema
from game.use_cases import (
    create_game,
    get_all_games_for_session,
)
from participation.schemas import participation_schema
from participation.use_cases import add_participation
from session.use_cases import (
    create_session,
    get_game_session,
    get_session,
    SessionClosedException,
    SessionOpenException,
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


@app.route('/session/<session_id>/game/', methods=['GET', 'POST'])
def game(session_id):
    get_session_or_404(session_id)

    if request.method == 'POST':
        data = validate(request.get_json(), game_schema)

        return _create_game(session_id, data)

    return jsonify(get_all_games_for_session(session_id))


@app.route('/slack/create_game/', methods=['POST'])
def slack_create_game():
    text = request.form.get('text')
    session_id, name, min_players, max_players = text.strip().split()
    min_players = int(min_players)
    max_players = int(max_players)

    data = validate({
        'name': name,
        'min_players': min_players,
        'max_players': max_players,
    }, game_schema)

    return _create_game(session_id, data)


@app.route('/session/<session_id>/participation/', methods=['POST'])
def participation(session_id):
    get_session_or_404(session_id)

    schema = Schema({
        Required('user_id'): All(str, Length(min=1)),
        Required('name'): All(str, Length(min=1)),
        Required('preferences'): list,
    })

    data = validate(request.get_json(), schema)
    return _create_participation(session_id, data)


@app.route('/slack/join_game/', methods=['POST'])
def slack_join_game():
    text = request.form.get('text')
    session_id, *preferences = text.strip().split()

    data = validate({
        'user_id': request.form['user_id'],
        'name': request.form['user_name'],
        'preferences': preferences,
    }, participation_schema)

    return _create_participation(session_id, data)


def _create_participation(session_id, validated_data):
    try:
        return jsonify(add_participation(
            session_id=session_id,
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            preferences=validated_data['preferences'],
        ))
    except SessionClosedException:
        abort(403)


@app.route('/session/<session_id>/game_session/', methods=['GET'])
def game_session(session_id):
    get_session_or_404(session_id)

    try:
        return jsonify(get_game_session(
            session_id=session_id,
        ))
    except SessionOpenException:
        abort(403)


def get_session_or_404(session_id):
    session = get_session(session_id)
    if not session:
        abort(404)
    return session


def validate(data, schema):
    try:
        return schema(data)
    except MultipleInvalid as e:
        abort(400)


def _create_game(session_id, validated_data):
    try:
        return jsonify(create_game(
            session_id=session_id,
            name=validated_data['name'],
            min_players=validated_data['min_players'],
            max_players=validated_data['max_players'],
        ))
    except SessionClosedException:
        abort(403)
