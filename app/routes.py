from app import app
import app.functions as funs
from flask import request


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


@app.route('/debug/ver_tok/<username>/<token>')  # FIXME: debug only!!!
def ver_tok(username, token):
    return funs.debug_verify(token, username)


@app.route('/admin/drop_tables/<secret_code>')
def drop_table(secret_code):
    return funs.drop_tables(secret_code)


@app.route('/game/get_state/<token>')
def game_get_state(token):
    return funs.get_game_state(token)


@app.route('/game/make_turn/<token>/<op_ind>', methods=['POST'])
def game_make_turn(token, op_ind):
    fun_inds = request.get_json()["fun_indexes"]
    return funs.make_turn(token, op_ind, fun_inds)