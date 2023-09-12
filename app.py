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

# Function to validate strings
def is_valid_string(value):
    return isinstance(value, str) or not name.isalpha() and len(value) <3

# Create a new resource (HTTP POST)
@app.route('/resources', methods=['POST'])
def create_resource():
    try:
        data = request.json
        name = data.get('name')
        specialization = data.get('specialization')
        programming_language = data.get('programming_language')

        if not is_valid_string(name) or not is_valid_string(specialization) or not is_valid_string(programming_language):
            return jsonify({"error": "Invalid data"}), 400

        # Insert the new resource into the database
        insert_query = "INSERT INTO resources (name, specialization, programming_language) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, specialization, programming_language))
        db_connection.commit()

        resource_id = cursor.lastrowid  # Get the ID of the newly inserted resource

        return jsonify({"message": "Resource created successfully", "data": {"id": resource_id, "name": name, "specialization": specialization, "programming_language": programming_language}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a resource by ID (HTTP GET)
@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource_by_id(resource_id):
    try:
        # Query the database for the resource with the given ID
        query = "SELECT id, name, specialization, programming_language FROM resources WHERE id = %s"
        cursor.execute(query, (resource_id,))
        resource = cursor.fetchone()

        if not resource:
            return jsonify({"error": "Resource not found"}), 404

        resource_data = {
            "id": resource[0],
            "name": resource[1],
            "specialization": resource[2],
            "programming_language": resource[3]
        }

        return jsonify({"data": resource_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a resource by ID (HTTP PUT)
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    try:
        data = request.json
        name = data.get('name')
        specialization = data.get('specialization')
        programming_language = data.get('programming_language')

        if not is_valid_string(name) or not is_valid_string(specialization) or not is_valid_string(programming_language):
            return jsonify({"error": "Invalid data"}), 400

        # Update the resource in the database
        update_query = "UPDATE resources SET name = %s, specialization = %s, programming_language = %s WHERE id = %s"
        cursor.execute(update_query, (name, specialization, programming_language, resource_id))
        db_connection.commit()

        return jsonify({"message": "Resource updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a resource by ID (HTTP DELETE)
@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    try:
        # Check if the resource exists before deleting it
        query = "SELECT id FROM resources WHERE id = %s"
        cursor.execute(query, (resource_id,))
        existing_resource = cursor.fetchone()

        if not existing_resource:
            return jsonify({"error": "Resource not found"}), 404

        # Delete the resource from the database
        delete_query = "DELETE FROM resources WHERE id = %s"
        cursor.execute(delete_query, (resource_id,))
        db_connection.commit()

        return jsonify({"message": "Resource deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
