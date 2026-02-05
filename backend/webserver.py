import os
from flask import Flask, request, jsonify, render_template_string
import sys

sys.path.append('..')
from database import db as db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

flaskapp = Flask(__name__)

global messages
messages: list[str] = []

@flaskapp.route('/')
def home():
    with open(os.path.join(FRONTEND_DIR, "index.html")) as f:
        html = f.read()
    return render_template_string(html)

@flaskapp.route('/styles.css')
def styles():
    with open(os.path.join(FRONTEND_DIR, "styles.css")) as f:
        css = f.read()
    return css, 200, {'Content-Type': 'text/css'}

@flaskapp.route('/create_account.js')
def create_account_js():
    with open(os.path.join(FRONTEND_DIR, "create_account.js")) as f:
        js = f.read()
    return js, 200, {'Content-Type': 'application/javascript'}

@flaskapp.route('/register', methods=['POST'])
def register():
    print("Received registration request")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    result = db.create_user(username, password)
    if result.is_error:
        return jsonify({"error": result.information}), 400
    
    return jsonify({"message": "Account created successfully!"}), 200

@flaskapp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400

    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    result = db.is_valid_user(username, password)

    if result:
        return jsonify({"status": "Success!"}), 200
    else:
        return jsonify({"status": "Invalid Username or Password!"}), 401

@flaskapp.route('/msg', methods=['POST'])
def msg():
    data = request.get_json()
    auth = data.get('auth')
    if not db.is_valid_user(auth.get('username'), auth.get('password')):
        return jsonify({"error": "Authentication failed"}), 401
    content = data.get('content')
    messages.append(content)
    return jsonify({"status": "Message received"}), 200

@flaskapp.route('/msg', methods=['GET'])
def get_msg():
    data = request.get_json()
    auth = data.get('auth')
    if not db.is_valid_user(auth.get('username'), auth.get('password')):
        return jsonify({"error": "Authentication failed"}), 401
    
    msgs = jsonify(messages)
    return jsonify({"messages": msgs}), 200


if __name__ == '__main__':
    print(sys.path)
    db.ensure_db()
    flaskapp.run(host='0.0.0.0', port=5000, debug=True)
