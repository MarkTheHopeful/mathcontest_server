from flask import Flask

app = Flask(__name__)


@app.route("/<username>", methods=["GET"])
def index(username):
    return f"Hello, {username}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5660")
