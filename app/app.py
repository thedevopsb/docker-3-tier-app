from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

def add_permissions_policy_header(response):
    response.headers['Permissions-Policy'] = (
        'attribution-reporting=(), '
        'run-ad-auction=(), '
        'join-ad-interest-group=(), '
        'browsing-topics=()'
    )
    return response

# MySQL Database Configuration
db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE'),
}
# Helper function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# API Endpoint to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert user into the database
        insert_query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, email))

        connection.commit()
        connection.close()

        return jsonify({'message': 'User added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint to get all users
@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        print (os.environ.get('MYSQL_HOST'),os.environ.get('MYSQL_USER'),os.environ.get('MYSQL_PASSWORD'),os.environ.get('MYSQL_DATABASE'))
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Retrieve all users from the database
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)
        users = cursor.fetchall()

        connection.close()

        return jsonify({'users': users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint to remove a user
@app.route('/remove_user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Delete user from the database
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))

        connection.commit()
        connection.close()

        return jsonify({'message': 'User removed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

