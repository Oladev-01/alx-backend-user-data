#!/usr/bin/env python3
from flask_httpauth import HTTPBasicAuth
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash


users = {
    "John": generate_password_hash("john123"),
    "Levi": generate_password_hash("Levi000")
}

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if not username and not password:
        username = request.args.get("username")
        password = request.args.get("password")
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def get_login():
    return f"Hello {auth.current_user()}"


if __name__ == "__main__":
    app.run(debug=True)

