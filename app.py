from flask import Flask, redirect, url_for, render_template
import json
from flask_socketio import SocketIO, emit
import time
import replicate
from environs import Env

env = Env()
env.read_env()

app = Flask(__name__)
socketio = SocketIO(app)

passage = "Tomato Juice"

@app.route('/')
def hello():
    return render_template("home.html", data=env("GITHUB"))

@socketio.on('long-running-event')
def handle_my_custom_event(input_json):
    time.sleep(1)
    global passage 
    passage = passage + input_json["data"]
    print(passage)
    emit('processing-finished', passage)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app)
    