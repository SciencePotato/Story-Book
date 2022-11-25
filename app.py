from flask import Flask, redirect, url_for, render_template
import replicate
from environs import Env

env = Env()
env.read_env()

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("home.html", data=env("GITHUB"))

if __name__ == "__main__":
    app.run(debug=True)
    