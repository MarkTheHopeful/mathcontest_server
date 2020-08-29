import app.functions as functions
from flask import request
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/v1/service/status', methods=['GET'])
def status():
    return functions.status()


@app.route('/api/v1/user/login/<username>/<password>', methods=['GET'])
def login(username, password):
    return functions.login(username, password)


@app.route('/api/v1/user/register/<username>/<password>', methods=['GET'])
def register(username, password):
    return functions.register(username, password)


@app.route('/api/v1/queue/put/<token>', methods=['GET'])
def put_user_in_queue(token):
    return functions.put_user_in_queue(token)


@app.route('/api/v1/queue/length', methods=['GET'])
def get_queue_len():
    return functions.get_queue_len()


@app.route('/api/v1/game/create/<token>', methods=['GET'])
def check_and_create(token):
    return functions.check_and_create(token)


@app.route('/api/v1/game/confirm/<token>', methods=['GET'])
def confirm_game_start(token):
    return functions.confirm_game_start(token)


@app.route('/api/v1/game/state/<token>/<is_latex>', methods=['GET'])
def game_get_state(token, is_latex):
    return functions.get_game_state(token, is_latex)


@app.route('/api/v1/game/turn/<token>/<operator_index>/<is_latex>', methods=['POST'])
def game_make_turn(token, operator_index, is_latex):
    indexes_function = request.get_json()["indexes_function"]
    return indexes_function.make_turn(token, operator_index, indexes_function, is_latex)


@app.route('/api/v1/admin/drop/<secret_code>', methods=['GET'])
def drop_table(secret_code):
    return functions.drop_tables(secret_code)
