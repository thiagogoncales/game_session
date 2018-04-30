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
from session.schemas import session_schema
from session.use_cases import (
    create_session,
    get_game_session,
    get_session,
    SessionClosedException,
    SessionOpenException,
    update_session,
)


app = Flask(__name__)


######################################################
##################### App routes #####################
######################################################

@app.route('/session/', methods=['POST'])
def session():
    return jsonify(create_session())


@app.route('/session/<session_id>/', methods=['GET', 'PUT'])
def session_detail(session_id):
    get_session_or_404(session_id)

    if request.method == 'PUT':
        data = validate(request.get_json(), session_schema)
        return jsonify(update_session(session_id, **data))
    return jsonify(get_session(session_id))


@app.route('/session/<session_id>/game/', methods=['GET', 'POST'])
def game(session_id):
    get_session_or_404(session_id)

    if request.method == 'POST':
        data = validate(request.get_json(), game_schema)

        try:
            return jsonify(create_game(
                session_id=session_id,
                name=data['name'],
                min_players=data['min_players'],
                max_players=data['max_players'],
            ))
        except SessionClosedException:
            abort(403)

    return jsonify(get_all_games_for_session(session_id))


@app.route('/session/<session_id>/participation/', methods=['POST'])
def participation(session_id):
    get_session_or_404(session_id)

    schema = Schema({
        Required('user_id'): All(str, Length(min=1)),
        Required('name'): All(str, Length(min=1)),
        Required('preferences'): list,
    })

    data = validate(request.get_json(), schema)

    try:
        return jsonify(add_participation(
            session_id=session_id,
            user_id=data['user_id'],
            name=data['name'],
            preferences=data['preferences'],
        ))
    except SessionClosedException:
       abort(403)


@app.route('/session/<session_id>/ame_session/', methods=['GET'])
def game_session(session_id):
    get_session_or_404(session_id)

    try:
        return jsonify(get_game_session(
            session_id=session_id,
        ))
    except SessionOpenException:
        abort(403)


######################################################
#################### Slack routes ####################
######################################################


@app.route('/slack/create_session/', methods=['POST'])
def slack_create_session():
    new_session = create_session()
    return create_slack_message(
        'New Session created {}'.format(new_session['session_id']),
    )


@app.route('/slack/add_game/', methods=['POST'])
def slack_add_game():
    text = request.form.get('text')
    session_id, name, min_players, max_players = text.strip().split()
    min_players = int(min_players)
    max_players = int(max_players)

    data = validate({
        'name': name,
        'min_players': min_players,
        'max_players': max_players,
    }, game_schema)

    try:
        new_game = create_game(
            session_id=session_id,
            name=data['name'],
            min_players=data['min_players'],
            max_players=data['max_players'],
        )
    except SessionClosedException:
       abort(403)

    return create_slack_message(
        'Game {name} ({game_id}) added to Session {session_id}'.format(
            name=new_game['name'],
            game_id=new_game['game_id'],
            session_id=session_id,
        ),
    )


@app.route('/slack/join_session/', methods=['POST'])
def slack_join_session():
    text = request.form.get('text')
    session_id, *preferences = text.strip().split()

    data = validate({
        'user_id': request.form['user_id'],
        'name': request.form['user_name'],
        'preferences': preferences,
    }, participation_schema)

    try:
        participation = add_participation(
            session_id=session_id,
            user_id=data['user_id'],
            name=data['name'],
            preferences=data['preferences'],
        )
    except SessionClosedException:
       abort(403)

    return create_slack_message(
        'Joined Session {session_id} with preferences ({preferences})'.format(
            session_id=session_id,
            preferences=', '.join(participation['preferences']),
        ),
        in_channel=False,
    )


@app.route('/slack/end_session/', methods=['POST'])
def slack_end_session():
    text = request.form.get('text')
    session_id = text.strip()

    data = validate({
        'is_active': False,
    }, session_schema)

    update_session(session_id, **data)

    game_sessions = get_game_session(
        session_id=session_id,
    )

    attachment_fields = [
        {
            'title': gs['game_id'],
            'value': ', '.join(gs['players']),
            'short': False,
        } for gs in game_sessions['game_sessions']
    ]

    attachment = {
        'fallback': 'These are the games that have enough interest',
        'title': 'Games',
        'text': 'These are the games with enough interest',
        'fields': attachment_fields,
    }


    return create_slack_message(
        'Session {session_id} ended!'.format(
            session_id=session_id,
        ),
        attachment=attachment,
    )


######################################################
###################### Helpers #######################
######################################################


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


def create_slack_message(message, in_channel=True, attachment={}):
    return jsonify({
        'response_type': 'in_channel' if in_channel else 'ephemeral',
        'text': message,
        'attachments': [attachment],
    })
