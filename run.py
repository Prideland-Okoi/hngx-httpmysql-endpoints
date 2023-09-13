import os, sys
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql = MySQL(app)

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
        language = data.get('language')

        if not is_valid_string(name) or not is_valid_string(track) or not is_valid_string(language):
            return jsonify({"error": "Invalid data"}), 400

        # Insert the new person into the database
        insert_query = "INSERT INTO studentrecord (name, track, language) VALUES (%s, %s, %s)"
        cur = mysql.connect().cursor()
        cur.execute(insert_query, (name, track, language))
        cur.close()

        person_id = cur.lastrowid  # Get the ID of the newly inserted person

        return jsonify({"message": "studentrecord created successfully", "data": {"id": person_id, "name": name, "track": track, "language": language}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a person by name (HTTP GET)
@app.route('/api/<name>', methods=['GET'])
def get_name(name):
    """Get a name by name."""
    try:
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        else:
            # Query the database for the person with the given name
            query = "SELECT * FROM studentrecord WHERE name = %s"
            cur = mysql.connect().cursor()
            cur.execute(query, (name,))
            result = cur.fetchone()
            cur.close()

            if result is None:
                return jsonify({'error': 'Name not found'})
            
            result_data = {
            "id": result[0],
            "name": result[1],
            "track": result[2],
            "language": result[3]
        }

            return jsonify({'data': result_data}), 200
    except Exception as e:
         return jsonify({"error": str(e)}), 500

# Update a person by ID (HTTP PUT)
@app.route('/api/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    try:
        data = request.json
        name = data.get('name')
        track = data.get('track')
        language = data.get('language')

        if not is_valid_string(name) or not is_valid_string(track) or not is_valid_string(language):
            return jsonify({"error": "Invalid data"}), 400

        # Update the person in the database
        update_query = "UPDATE studentrecord SET name = %s, track = %s, language = %s WHERE id = %s"
        cur = mysql.connect().cursor()
        cur.execute(update_query, (name, track, language, person_id))
        #cur.commit()
        cur.close()

        return jsonify({"message": "person updated successfully", "data": {"id": person_id, "name": name, "track": track, "language": language}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a person by ID (HTTP DELETE)
@app.route('/api/name', methods=['DELETE'])
def delete_person(person):
    try:
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        # Check if the person exists before deleting it
        query = "SELECT name FROM studentrecord WHERE name = %s"
        cur = mysql.connect().cursor()
        cur.execute(query, (person,))
        existing_person = cur.fetchone()

        if not existing_person:
            return jsonify({"error": "Records of person not found", "data": {"person": person}}), 404

        # Delete the person from the database
        delete_query = "DELETE FROM studentrecord WHERE name = %s"
        cur = mysql.connect().cursor()
        cur.execute(delete_query, (person,))
        #db_connection.commit()
        cur.close()

        return jsonify({"message": "person deleted successfully", "data": {"id": person_id, "name": name, "track": track, "language": language}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
