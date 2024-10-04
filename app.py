from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['userdb']

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify({'status': 'success', 'users': users})

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    db.users.insert_one(user_data)
    return jsonify({'status': 'success', 'message': 'User created successfully.'})

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    user['_id'] = str(user['_id'])
    return jsonify({'status': 'success', 'user': user})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.get_json()
    db.users.update_one({'_id': ObjectId(id)}, {'$set': user_data})
    return jsonify({'status': 'success', 'message': 'User updated successfully.'})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'status': 'success', 'message': 'User deleted successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
