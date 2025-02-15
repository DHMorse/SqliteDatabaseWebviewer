from flask import Flask, jsonify, request, render_template
import sqlite3
import json

app = Flask(__name__)

# Database configuration
DATABASE = '/home/botuser/Omniplexium-Eternal/discorddb.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables dictionary-like rows
    return conn

@app.route('/')
def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template('index.html', tables=tables)

# Function to transform the 'items' field
def transform_data(data):
    for item in data:
        if 'items' in item:
            item['items'] = json.loads(item['items'])
    return data

@app.route('/users')
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_id = request.args.get('userId')
        
        if user_id:
            cursor.execute("SELECT * FROM users WHERE userId = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM users")
        
        columns = [description[0] for description in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in rows:
            if 'userId' in row:
                row['userId'] = int(row['userId'])
        
        rows = transform_data(rows)
        
        if user_id and not rows:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(rows)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/<table_name>')
def show_table_contents(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in rows:
            if 'userId' in row:
                row['userId'] = int(row['userId'])
        
        rows = transform_data(rows)
        return jsonify(rows)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
