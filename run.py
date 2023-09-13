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

# Create a new student (HTTP POST)
@app.route('/api', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        name = data.get('name')
        track = data.get('track')

        if not is_valid_string(name) or not is_valid_string(track):
            return jsonify({"error": "Invalid data"}), 400

        # Insert the new student into the database
        insert_query = "INSERT INTO studentlog (name, track) VALUES (%s, %s)"
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute(insert_query, (name, track))
        #cursor.close()

        # Commit changes to the database
        connection.commit()

        student_id = cursor.lastrowid  # Get the ID of the newly inserted student

        return jsonify({"message": "studentlog created successfully", "student log": {"id": student_id, "name": name, "track": track,}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a student by name (HTTP GET)
@app.route('/api/<name>', methods=['GET'])
def get_student(name):
    """Get student by name."""
    try:
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        else:
            # Query the database for the student with the given name
            query = "SELECT * FROM studentlog WHERE name = %s"
            cur = mysql.connect().cursor()
            cur.execute(query, (name))
            student = cur.fetchone()
            cur.close()

            if student is None:
                return jsonify({'error': 'Name not found'})
            
            student_data = {
            "id": student[0],
            "name": student[1],
            "track": student[2]
            }

            return jsonify({'student info': student_data}), 200
    except Exception as e:
         return jsonify({"error": str(e)}), 500

# Get all the students create (HTTP GET)
@app.route('/api/', methods=['GET'])
# for testing purpose
def get_names():
    """Get all names."""
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM studentlog')
    names = cursor.fetchall()
    cursor.close()

    return jsonify(names)

# Update a student by name (HTTP PUT)
@app.route('/api/<name>', methods=['PUT'])
def update_student(name):
    try:
        #data = request.json.get('data')
        data = request.get_json()
        new_name = data.get('name')
        new_track = data.get('track')

        if not is_valid_string(name):
            return jsonify({"error": "Invalid data"}), 400
        else:
            # Update the person in the database
            update_query = "UPDATE studentlog SET name = %s, track = %s WHERE name = %s"
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(update_query, (new_name, new_track, name))
            connection.commit()
            return jsonify({"message": "person updated successfully", "student info": new_name}), 200
    except Exception as e:
                return jsonify({"error": str(e)}), 500

# Delete a student by name (HTTP DELETE)
@app.route('/api/<name>', methods=['DELETE'])
def delete_student(name):
    try:
        if not isinstance(name, str) or not name.isalpha():
            return jsonify({'error': 'Invalid name format'})
        else:
            # Check if the student exists before deleting it
            query = "SELECT name FROM studentlog WHERE name = %s"
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(query, (name))
            existing_student = cursor.fetchone()

            if not existing_student:
                return jsonify({"error": "Records of person not found", "search": {"name": name}}), 404
            else:
                # Delete the person from the database
                delete_query = "DELETE FROM studentlog WHERE name = %s"
                connection = mysql.connect()
                cursor = connection.cursor()
                cursor.execute(delete_query, (name))
                connection.commit()
                #cursor.close()

                return jsonify({"message": "student deleted successfully", "data": {"name": name }}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
