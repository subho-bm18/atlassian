from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory data store (simulates a database)
users = {}

# Home route
@app.route('/')
def home():
    return "Welcome to the User Management API!"

# Get user details
@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = users.get(username)
    if user:
        return jsonify({"username": username, "details": user}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "Username is required"}), 400

    username = data['username']
    if username in users:
        return jsonify({"error": "User already exists"}), 409

    users[username] = {
        "email": data.get("email", ""),
        "age": data.get("age", 0)
    }
    return jsonify({"message": "User created", "user": users[username]}), 201

# Update an existing user
@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    if username not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[username].update({
        "email": data.get("email", users[username]["email"]),
        "age": data.get("age", users[username]["age"])
    })
    return jsonify({"message": "User updated", "user": users[username]}), 200

# Delete a user
@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    if username not in users:
        return jsonify({"error": "User not found"}), 404

    del users[username]
    return jsonify({"message": f"User {username} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
