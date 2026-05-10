from flask import Flask, jsonify, render_template, request
import os
import pymysql

app = Flask(__name__)

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS example_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
"""

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'dbuser'),
        password=os.environ.get('DB_PASSWORD', ''),
        db=os.environ.get('DB_NAME', 'devprojdb'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

def ensure_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(CREATE_TABLE_QUERY)
    connection.commit()

@app.route('/health')
def health():
    return "Up & Running"

@app.route('/create_table')
def create_table():
    try:
        connection = get_db_connection()
        ensure_table(connection)
        connection.close()
        return "Table created successfully"
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/insert_record', methods=['POST'])
def insert_record():
    try:
        name = request.json['name']
        connection = get_db_connection()
        ensure_table(connection)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO example_table (name) VALUES (%s)", (name,))
        connection.commit()
        connection.close()
        return jsonify({"message": "Record inserted successfully"})
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/data')
def data():
    try:
        connection = get_db_connection()
        ensure_table(connection)
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM example_table')
            result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# UI route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
