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
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.valid_login(email, password)
        session_id = AUTH.create_session(email)
        msg = {"email": email, "message": "logged in"}
        response = jsonify(msg)

        response.set_cookie("session_id", session_id)

        return response
    except (InvalidRequestError, NoResultFound):
        abort(401)

@app.route('/sessions', strict_slashes=False, methods=['DELETE'])
def del_session():
    """deletes a session"""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except (NoResultFound, InvalidRequestError, ValueError):
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
