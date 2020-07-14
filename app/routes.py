from app import app
import app.functions as funs


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
