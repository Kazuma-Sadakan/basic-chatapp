import os 
import time 

from dotenv import load_dotenv
import requests
from flask import Flask, request, redirect, url_for, render_template, jsonify

from opt.src.database import ClientDB, MessageDB
from opt.src.server.client import ClientThread, Controller
load_dotenv()

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

app = Flask(__name__)
client_thread = ClientThread(HOST, PORT)

BASE_DIR = os.path.dirname(__file__)
CLIENT_DB = os.path.join(BASE_DIR, "client.db")
MESSAGE_DB = os.path.join(BASE_DIR, "message.db")
client_db = ClientDB(CLIENT_DB)
message_db = MessageDB(MESSAGE_DB)

@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    print(request_data)
    name = request_data["message"].get("name", None)
    if name is None:
        response = {
            "message": "username cannot be empty"
        }
        return jsonify(response), 400

    success = client_db.save(username = name, timestamp = time.time())
    if not success:
        response = {
            "message": "username already exists"
        }
        return jsonify(response), 400

    if name:
        client_thread.start()
        client_thread.controller(Controller.CONNECT, name)
        client_thread.controller(Controller.SEND, name)
        return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat", methods=["GET"])
def chat():
    data = message_db.get_all()
    response = {
        "message": data
    }
    return jsonify(response), 200

@app.route("/message", methods=["GET"])
def message():
    client_thread.controller(Controller.RECEIVE, "")
    if not client_thread.msg_q.empty():
        msg = client_thread.msg_q.get()
        print(msg)
        return jsonify(msg), 200
    response = {
        "message": ""
    }
    return jsonify(response), 200

@app.route("/message", methods=["POST"])
def send_message():
    required_data = request.get_json()
    if required_data["message"] == "q":
        requests.post("/close")
    client_thread.controller(Controller.SEND, required_data)

@app.route("/close", methods=["POST"])
def close():
    client_thread.controller(Controller.CLOSE, "")
    return redirect("/login.html")

    

