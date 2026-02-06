## Routes login attempts and serves the account creation page.

import os
from flask import Flask, request, jsonify, render_template_string
import sys

sys.path.append('..')
from database import admin as admin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

flaskapp = Flask(__name__)

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

    result = admin.create_user(username, password)
    if result.is_error:
        return jsonify({"message": result.information}), 400
    
    return jsonify({"message": "Account created successfully!"}), 200

@flaskapp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Expected JSON"}), 400

    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    result = admin.is_valid_user(username, password)

    if result:
        return jsonify({"status": "Success!"}), 200
    else:
        return jsonify({"status": "Invalid Username or Password!"}), 401

if __name__ == '__main__':
    print(sys.path)
    admin.ensure_db()
    flaskapp.run(host='0.0.0.0', port=5000, debug=True)
