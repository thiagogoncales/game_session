from flask import (
    Flask,
    jsonify,
    request,
)

from session.use_cases import (
    create_session,
)


app = Flask(__name__)


@app.route('/session/', methods=['POST'])
def game_session():
    return jsonify(create_session())
