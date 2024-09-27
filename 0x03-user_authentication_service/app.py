#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from auth import Auth
from flask import (
    Flask, jsonify,
    make_response, request,
    abort, redirect
)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ Base route for authentication service API """
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """Registers a new user if it does not exist before"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


@app.route('/sessions', methods=['POST'])
def set_session() -> str:
    """ Logs in a user and returns session ID """
    email = request.form.get('email')
    password = request.form.get('password')
    AUTH.valid_login(email, password)
    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)

    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """destroy from session"""
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ If the user exist, respond with a 200
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    msg = {"email": user.email}

    return jsonify(msg), 200


@app.route('/reset_password', method=['POST'])
def reset_token() -> str:
    """reset token"""
    email = request.form.get('email')
    if email is None:
        abort(403)
    try:
        r_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": r_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
