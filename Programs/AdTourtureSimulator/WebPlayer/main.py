from cgitb import text
from threading import Lock
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from eyetrackerForKivy import *
import requests

async_mode = None

app = Flask(__name__)
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

def listen():
    while True:
        socketio.sleep(2)
        socketio.emit(runEyetrackerForReal())


import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("Programs/AdTourtureSimulator/WebPlayer/key2.json")
firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://accounts-883b3-default-rtdb.firebaseio.com'})

from firebase_admin import db

page = "home"

@app.route('/')
def home():
    global page
    page = "home"
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    global page
    print('Entered Login')
    if request.method == "POST" and page == "login":
        user = request.form["name"]
        Pass = request.form["pass"]
        
        ref = db.reference("/")
        data = ref.get()

        valid = False

        for name in data:
            if name == user:
                ref = db.reference("/" + name)
                data = ref.get()
                if data["Password"] == Pass:
                    valid = True
                    break
                break

        if valid:
            print('VALID!')
            return redirect(url_for("user", usr=user))
        else:
            return redirect(url_for("login", usr=user))
    else:
        page = "login"
        return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    global page
    print(page)
    if request.method == "POST" and page == "signup":
        username = request.form['user']
        password = request.form['password']

        ref = db.reference("/" + username)
        ref.set({"Password": password})

        return redirect(url_for("login", usr=user))
    else:
        page = "signup"
        return render_template("signup.html")


@app.route('/<usr>')
def user(usr):
    return render_template("user.html", user=usr, videos={"SpongeBob", "Squarepants"}, async_mode=socketio.async_mode)


if __name__ == '__main__':
    app.run(debug=True)