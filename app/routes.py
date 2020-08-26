import app.functions as funs
from flask import request
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/status', methods=['GET'])
def status():
    return funs.status()


@app.route('/login/<username>/<password>')  # FIXME: mmm, security
def login(username, password):
    return funs.login(username, password)


@app.route('/register/<username>/<password>')  # FIXME: mmm, security
def register(username, password):
    return funs.register(username, password)


@app.route('/start_game/<invitor_token>/<invited_username>')  # FIXME: this function will be replaced
def start_game(invitor_token, invited_username):
    return funs.start_game(invitor_token, invited_username)


@app.route('/put_user_in_queue/<token>')
def put_user_in_queue(token):
    return funs.put_user_in_queue(token)


@app.route('/admin/drop_tables/<secret_code>')
def drop_table(secret_code):
    return funs.drop_tables(secret_code)


@app.route('/game/get_state/<token>/<is_latex>')
def game_get_state(token, is_latex):
    return funs.get_game_state(token, is_latex)


@app.route('/game/make_turn/<token>/<op_ind>/<is_latex>', methods=['POST'])
def game_make_turn(token, op_ind, is_latex):
    fun_inds = request.get_json()["fun_indexes"]
    return funs.make_turn(token, op_ind, fun_inds, is_latex)
