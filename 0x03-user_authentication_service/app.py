#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth

# Create an instance of the Flask class
app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def hello():
    """ Define a route for the GET method """
    # Return a JSON payload with a message
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ function that implements the POST /users route """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ function to respond to the POST /sessions route. """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": "<user email>",
                             "message": "logged in"}), 200)

    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ function to respond to the DELETE /sessions route. """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile() -> str:
    """ function that respond to the GET /profile route. """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    # If the user exists
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ function that respond to the POST /reset_password route. """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """function that respond to the PUT /reset_password route"""

    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    """ Run the app if this module is executed """
    app.run(host="0.0.0.0", port="5000")
