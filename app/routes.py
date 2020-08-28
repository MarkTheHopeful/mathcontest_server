import app.functions as funs
from flask import request
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/v1/service/status', methods=['GET'])
def status():
    return funs.status()


@app.route('/api/v1/user/login/<username>/<password>', methods=['GET'])
def login(username, password):
    return funs.login(username, password)


@app.route('/api/v1/user/register/<username>/<password>', methods=['GET'])
def register(username, password):
    return funs.register(username, password)


@app.route('/api/v1/queue/put/<token>', methods=['GET'])
def put_user_in_queue(token):
    return funs.put_user_in_queue(token)


@app.route('/api/v1/queue/length', methods=['GET'])
def get_queue_len():
    return funs.get_queue_len()


@app.route('/api/v1/game/create/<token>', methods=['GET'])
def check_and_create(token):
    return funs.check_and_create(token)


@app.route('/api/v1/game/confirm/<token>', methods=['GET'])
def confirm_game_start(token):
    return funs.confirm_game_start(token)


@app.route('/api/v1/game/state/<token>/<is_latex>', methods=['GET'])
def game_get_state(token, is_latex):
    return funs.get_game_state(token, is_latex)


@app.route('/api/v1/game/turn/<token>/<op_ind>/<is_latex>', methods=['POST'])
def game_make_turn(token, op_ind, is_latex):
    fun_inds = request.get_json()["fun_indexes"]
    return funs.make_turn(token, op_ind, fun_inds, is_latex)


@app.route('/api/v1/admin/drop/<secret_code>', methods=['GET'])
def drop_table(secret_code):
    return funs.drop_tables(secret_code)
