from flask import Flask, jsonify, request, send_from_directory
import database as db

app = Flask(__name__)

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

@app.route('/api')
def api_home():
    return jsonify(message="API fromm FLASK is running."), 200

@app.route('/api/users', methods=['GET'])
def list_users():
    try:
        users = db.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve users"}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        print(f"Received data: {data}") 
        
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
        
        name = data['name']
        email = data.get('email', '')
        age = data.get('age', 0)
        
        print(f"Creating user: name={name}, email={email}, age={age}") 
        new_user = db.create_user(name, email, age)
        print(f"Created user: {new_user}")  
        return jsonify(new_user), 201
        
    except Exception as e:
        print(f"Error creating user: {e}") 
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        
        current_user = db.get_user_by_id(id)
        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        name = data.get('name', current_user['name'])
        email = data.get('email', current_user['email'])
        age = data.get('age', current_user['age'])
        
        updated_user = db.update_user(id, name, email, age)
        if updated_user:
            return jsonify(updated_user), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": "Failed to update user"}), 500

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        deleted_user = db.delete_user(id)
        if deleted_user:
            return jsonify({
                "message": "User deleted successfully", 
                "user": deleted_user
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": "Failed to delete user"}), 500

if __name__ == '__main__':
    app.run(debug = True)

