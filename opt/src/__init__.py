# import os 

# from dotenv import load_dotenv
# import requests
# from flask import Flask, request, redirect, url_for, render_template, jsonify

# from .server.client import ClientThread, Controller
# load_dotenv()

# HOST = os.environ.get("HOST")
# PORT = int(os.environ.get("PORT"))

# app = Flask(__name__)
# client_thread = ClientThread(HOST, PORT)


# @app.route("/login", methods=["POST"])
# def login():
#     request_data = request.get_json()
#     name = request_data["message"].get("name", None)
#     print(name)
#     if name:
#         client_thread.start()
#         client_thread.controller(Controller.CONNECT, name)
#         client_thread.controller(Controller.SEND, name)
#         return redirect(url_for("chat"))
#     return render_template("login.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     return render_template("chat.html")

# @app.route("/message", methods=["GET"])
# def message():
#     client_thread.controller(Controller.RECEIVE, "")
#     if not client_thread.msg_q.empty():
#         msg = client_thread.msg_q.get()
#         return jsonify(msg)

# @app.route("/message", methods=["POST"])
# def send_message():
#     required_data = request.get_json()
#     if required_data["message"] == "q":
#         requests.post("/close")
#     client_thread.controller(Controller.SEND, required_data)

# @app.route("/close", methods=["POST"])
# def close():
#     client_thread.controller(Controller.CLOSE, "")
#     return redirect("/login.html")

    

