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
    update_session,
)


app = Flask(__name__)


@app.route('/session/', methods=['POST'])
def session():
    return jsonify(create_session())


@app.route('/session/<session_id>/', methods=['GET', 'PUT'])
def session_detail(session_id):
    get_session_or_404(session_id)
    if request.method == 'PUT':
        data = request.get_json()
        return jsonify(update_session(session_id, **data))
    return jsonify(get_session(session_id))


@app.route('/session/<session_id>/game/', methods=['POST'])
def game(session_id):
    get_session_or_404(session_id)

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

def get_session_or_404(session_id):
    session = get_session(session_id)
    if not session:
        abort(404)
    return session
