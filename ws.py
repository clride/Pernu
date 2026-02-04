from flask import Flask, request, jsonify, render_template_string

from database import db

app = Flask(__name__)

global messages
messages: list[str] = []

# Serve your login page
@app.route('/')
def home():
    with open("frontend/index.html") as f:
        html = f.read()
    return render_template_string(html)

@app.route('/styles.css')
def styles():
    with open("frontend/styles.css") as f:
        css = f.read()
    return css, 200, {'Content-Type': 'text/css'}

@app.route('/create_account.js')
def create_account_js():
    with open("frontend/create_account.js") as f:
        js = f.read()
    return js, 200, {'Content-Type': 'application/javascript'}

# Handle account creation
@app.route('/register', methods=['POST'])
def register():
    print("Received registration request")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    result = db.create_user(username, password)
    if result.is_error:
        return jsonify({"error": result.information}), 400
    
    return jsonify({"message": "Account created successfully!"}), 200

# Handle account login
@app.route('/login', methods=['POST'])
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

@app.route('/msg', methods=['POST'])
def msg():
    data = request.get_json()
    auth = data.get('auth')
    if not db.is_valid_user(auth.get('username'), auth.get('password')):
        return jsonify({"error": "Authentication failed"}), 401
    content = data.get('content')
    messages.append(content)
    return jsonify({"status": "Message received"}), 200

@app.route('/msg', methods=['GET'])
def get_msg():
    data = request.get_json()
    auth = data.get('auth')
    if not db.is_valid_user(auth.get('username'), auth.get('password')):
        return jsonify({"error": "Authentication failed"}), 401
    
    msgs = jsonify(messages)
    return jsonify({"messages": msgs}), 200


if __name__ == '__main__':
    # Run local server
    db.ensure_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
