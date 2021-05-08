from flask import Flask

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

# execute command in windows
# set FLASK_APP=app.py
# set FLASK_DEBUG=1
# flask run
