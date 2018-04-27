from flask import (
    Flask,
    jsonify,
    request,
)

from session.use_cases import (
    create_session,
    get_all_sessions,
)


app = Flask(__name__)


@app.route('/session/', methods=['GET', 'POST'])
def game_session():
    if request.method == 'POST':
        return jsonify(create_session())
    return jsonify(get_all_sessions())
