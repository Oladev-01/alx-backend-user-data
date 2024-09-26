#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from auth import Auth
from flask import (
    Flask, jsonify,
    make_response, request,
    abort
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


@app.route('/sessions', strict_slashes=False, methods=['POST'])
def set_session():
    """Sets the session for the request."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if not AUTH.valid_login(email, password):
            abort(401)  # Invalid login credentials
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    except (NoResultFound, InvalidRequestError):
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
