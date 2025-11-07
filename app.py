import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId  # This is needed to work with MongoDB's _id
import sys # Import sys for printing error messages

# --- 1. SET UP THE FLASK APP ---
app = Flask(__name__)

# --- 2. SET UP THE MONGODB CONNECTION ---

# 🛑 CRITICAL: PASTE YOUR MONGODB ATLAS CONNECTION STRING HERE
# Replace <username> and <password> with your actual database user credentials.
# Replace 'notes-cluster.abc12.mongodb.net' with your cluster's address.
# The 'notes_db' at the end is the name of the database that will be created.
try:
    # ADD THESE 4 NEW LINES:
    MONGO_URI = os.environ.get('MONGO_URI')
    if not MONGO_URI:
        print("❌ ERROR: MONGO_URI environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # This line was already here:
    client = MongoClient(MONGO_URI)
    client = MongoClient(MONGO_URI)
    db = client.notes_db # The database
    notes_collection = db.notes  # The collection (like a table)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas!")

except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}", file=sys.stderr)
    # If we can't connect, we probably shouldn't continue.
    # For a real app, you'd have more robust error handling.
    sys.exit(1)


# --- 3. DEFINE THE API ENDPOINTS (ROUTES) ---

# [C]REATE A NEW NOTE
@app.route('/notes', methods=['POST'])
def create_note():
    try:
        data = request.get_json()
        
        # Basic validation
        if 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Missing title or content'}), 400

        new_note = {
            'title': data['title'],
            'content': data['content']
        }
        
        # Insert into the database
        result = notes_collection.insert_one(new_note)
        
        # Return the new note's ID
        return jsonify({'message': 'Note created', 'id': str(result.inserted_id)}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# [R]EAD ALL NOTES
@app.route('/notes', methods=['GET'])
def get_all_notes():
    try:
        all_notes = []
        for note in notes_collection.find():
            # Convert the MongoDB _id (ObjectId) to a string
            note['_id'] = str(note['_id'])
            all_notes.append(note)
            
        return jsonify(all_notes), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# [R]EAD ONE NOTE BY ID
@app.route('/notes/<id>', methods=['GET'])
def get_one_note(id):
    try:
        # Convert the string ID back to an ObjectId
        note = notes_collection.find_one({'_id': ObjectId(id)})
        
        if note:
            note['_id'] = str(note['_id'])
            return jsonify(note), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
            
    except Exception as e:
        # This will catch errors like "InvalidId" if the ID format is wrong
        return jsonify({'error': 'Invalid ID or note not found', 'details': str(e)}), 404

# [U]PDATE A NOTE BY ID
@app.route('/notes/<id>', methods=['PUT'])
def update_note(id):
    try:
        data = request.get_json()
        
        # Basic validation
        if 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Missing title or content'}), 400
            
        new_values = {
            '$set': {
                'title': data['title'],
                'content': data['content']
            }
        }
        
        # Find the note by ID and update it
        result = notes_collection.update_one({'_id': ObjectId(id)}, new_values)
        
        if result.matched_count == 1:
            return jsonify({'message': 'Note updated successfully'}), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Invalid ID or update failed', 'details': str(e)}), 400

# [D]ELETE A NOTE BY ID
@app.route('/notes/<id>', methods=['DELETE'])
def delete_note(id):
    try:
        # Find the note by ID and delete it
        result = notes_collection.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 1:
            return jsonify({'message': 'Note deleted successfully'}), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Invalid ID or delete failed', 'details': str(e)}), 400


# --- 4. RUN THE FLASK APP ---
if __name__ == '__main__':
    # debug=True will auto-reload the server when you save the file

    app.run(debug=True)
