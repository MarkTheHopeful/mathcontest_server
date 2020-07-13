from app import app
import app.functions as funs


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/status', methods=['GET'])
def status():
    return funs.status()


@app.route('/login/<username>/<passhash>')
def login(username, passhash):
    return funs.login(username, passhash)

@app.route('/register/<username>/<passhash>')
def register(username, passhash):
    return funs.register(username, passhash)