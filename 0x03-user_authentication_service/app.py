#!/usr/bin/env python3
"""Basic Flask app """
from flask import Flask, jsonify, request, abort, Response
from auth import Auth
from typing import Tuple

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
AUTH = Auth()


@app.route('/', methods=["GET"])
def index() -> Response:
    """Return greetings"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def create_user() -> Tuple['Response', 'int']:
    """Create a new user"""

    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400, "Missing")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/login', methods=['POST'])
def login() -> Response:
    data = request.form
    if 'email' not in data:
        return jsonify({"message": "email is required"}), 400
    if 'password' not in data:
        return jsonify('{"message": "password is required"}'), 400
    else:
        email = data['email']
        password = data['password']
        if AUTH.valid_login(email=email, password=password) is False:
            return abort(401, "Invalid credentials")
        else:
            session_id = AUTH.create_session(email=email)
            response = jsonify({
                'email': email,
                "message": "logged in successfully"
            })
            response.set_cookie('session_id', session_id)
            return response


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """respond to the POST create a new session for the user"""
    form_data = request.form
    if "email" not in form_data:
        return jsonify({"message": "email required"}), 400
    elif "password" not in form_data:
        return jsonify({"message": "password required"}), 400
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if AUTH.valid_login(email, password) is False:
            abort(401)
        else:
            session_id = AUTH.create_session(email)
            response = jsonify({
                "email": email,
                "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
