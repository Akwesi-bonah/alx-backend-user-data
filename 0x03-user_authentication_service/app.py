#!/usr/bin/env python3
"""a basic Flask app.
"""
from flask import Flask, jsonify, abort, request, redirect, Response
from auth import Auth
from typing import Union

app = Flask(__name__)
AUTH = Auth()
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET'])
def home() -> Response:
    """index to display greetings"""
    form_data = {"message": "Bienvenue"}

    return jsonify(form_data), 200


@app.route('/users', methods=['POST'])
def register_user() -> Union[str, Response]:
    """to record into db new user"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Union[str, Response]:
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def log_out() -> Union[None, Response]:
    """user with the requested session ID get the session destroyed"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """find the user respond with a 200 HTTP status"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """respond to the POST /reset_password to reset password"""
    try:
        email = request.form["email"]
    except KeyError:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """respond to the PUT /reset_password to update password"""
    try:
        email = request.form["email"]
        reset_token = request.form["reset_token"]
        new_password = request.form["new_password"]
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
