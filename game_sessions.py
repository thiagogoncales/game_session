from flask import (
    abort,
    Flask,
    jsonify,
    request,
)

from game.use_cases import (
    create_game,
    SessionClosedException,
)
from session.use_cases import (
    create_session,
    get_session,
)


app = Flask(__name__)


@app.route('/session/', methods=['POST'])
def session():
    return jsonify(create_session())


@app.route('/session/<session_id>/game/', methods=['POST'])
def game(session_id):
    if not get_session(session_id):
        abort(404)

    data = request.get_json()

    try:
        return jsonify(create_game(
            session_id=session_id,
            name=data['name'],
            min_players=data['min_players'],
            max_players=data['max_players'],
        ))
    except SessionClosedException:
        abort(403)
