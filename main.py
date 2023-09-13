import os, sys
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration (replace with your database credentials)
db_config = {
    "host": "sql3.freesqldatabase.com",
    "user": "sql3645708",
    "password": "XgJcg71W7r",
    "database": "sql3645708"
}

# Create a MySQL database connection
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Create a table for hngx student if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS studentlog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    track VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_query)
db_connection.commit()

# Function to validate strings
def is_valid_string(value):
    return isinstance(value, str) or not name.isalpha()

# Create a new person (HTTP POST)
@app.route('/api', methods=['POST'])
def create_person():
    try:
        data = request.get_json()
        name = data.get('name')
        track = data.get('track')
        #language = data.get('language')

        if not is_valid_string(name) or not is_valid_string(track):# or not is_valid_string(language):
            return jsonify({"error": "Invalid data"}), 400

        # Insert the new person into the database
        insert_query = "INSERT INTO studentlog (name, track) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, track))
        db_connection.commit()

        person_id = cursor.lastrowid  # Get the ID of the newly inserted person

        return jsonify({"message": "studentlog created successfully", "student": {"id": person_id, "name": name, "track": track}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a person by ID (HTTP GET)
@app.route('/api/<name>', methods=['GET'])
def get_name(name):
    """Get a name by name."""
    try:
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        else:
            # Query the database for the person with the given name
            query = "SELECT * FROM studentlog WHERE name = %s"
            cursor.execute(query, (name,))
            student = cursor.fetchone()
            cursor.close()

            if student is None:
                return jsonify({'error': 'Name not found'})
            
            student_data = {
            "id": student[0],
            "name": student[1],
            "track": student[2]
        }

            return jsonify({'data': student_data}), 200
    except Exception as e:
         return jsonify({"error": str(e)}), 500

# Update a person by ID (HTTP PUT)
@app.route('/api/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    try:
        data = request.json
        name = data.get('name')
        track = data.get('track')
        #language = data.get('language')

        if not is_valid_string(name) or not is_valid_string(track):# or not is_valid_string(language):
            return jsonify({"error": "Invalid data"}), 400

        # Update the person in the database
        # UPDATE `studentlog` SET `name` = REPLACE(`name`, 'radis', 'justin') WHERE `name` LIKE '%radis%' COLLATE utf8mb4_bin
        update_query = "UPDATE studentlog SET name = %s, track = %s WHERE id = %s"
        cursor.execute(update_query, (name, track, language, person_id))
        db_connection.commit()

        return jsonify({"message": "person updated successfully", "student": {"id": person_id, "name": name, "track": track}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a person by ID (HTTP DELETE)
@app.route('/api/name', methods=['DELETE'])
def delete_person(name):
    try:
        #name = request.args.get('name')
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        # Check if the person exists before deleting it
        query = "SELECT name FROM studentlog WHERE name = %s"
        cursor.execute(query, (name,))
        existing_person = cursor.fetchone()

        if not existing_person:
            return jsonify({"error": "person not found", "data": {"person": name}}), 404

        # Delete the person from the database
        delete_query = "DELETE FROM studentlog WHERE name = %s"
        cursor.execute(delete_query, (name,))
        db_connection.commit()

        return jsonify({"message": "person deleted successfully", "student": { "id":person_id, "name": name, "track": track}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
