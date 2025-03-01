from flask import Flask, jsonify, render_template, request
from threading import Thread
import sqlite3

from helperFunctions import *

loggedInUsers: list[tuple[str, str, bool]] = []

app = Flask(__name__)

@app.route('/')
def index():
    global DATABASE, PASSWORD_PROTECTION, USERS
    
    if not isClientLoggedIn(loggedInUsers) and PASSWORD_PROTECTION:
        return render_template('login.html'), 302
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
        
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    if PASSWORD_PROTECTION:
        clientIp = request.remote_addr
        
        for user in loggedInUsers:
            if user[0] == clientIp:
                username = user[1]
                break
        
        if not username:
            return render_template('login.html'), 302

        USER = USERS[username]
        
        tables = [table for table in tables if hasPermission(USER, table)]

    return render_template('index.html', tables=tables)

@app.route('/<tableName>')
def show_table_contents(tableName):
    global DATABASE, PASSWORD_PROTECTION, USERS

    if not isClientLoggedIn(loggedInUsers) and PASSWORD_PROTECTION:
        return render_template('login.html'), 302, {'Location': '/'}
    
    if PASSWORD_PROTECTION:
        clientIp = request.remote_addr
        
        for user in loggedInUsers:
            if user[0] == clientIp:
                username = user[1]
                break
        
        if not username:
            return render_template('login.html'), 302, {'Location': '/'}

        user = USERS[username]
        
        if not hasPermission(user, tableName):
            return render_template('index.html'), 302, {'Location': '/'}

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {tableName}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
        
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('table.html', tableName=tableName, columns=columns, rows=rows)

@app.route('/login', methods=['POST'])
def login():
    global PASSWORD_PROTECTION, USERS, loggedInUsers
    
    if not PASSWORD_PROTECTION:
        return jsonify({'error': 'Password protection is not enabled'}), 403
    
    clientIp = request.remote_addr
    
    # Check if IP is already logged in
    if any(user[0] == clientIp for user in loggedInUsers):
        return jsonify({'error': 'Already logged in from this IP address'}), 403
    
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if PASSWORD_PROTECTION:
        if not USERS.get(username):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if USERS[username]['password'] == password:
            loggedInUsers.append((clientIp, username, True))
            return jsonify({'success': 'Login successful!'}), 200
        
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    
    else:
        loggedInUsers.append((clientIp, username, True))
        return jsonify({'success': 'Login successful!'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    global loggedInUsers

    clientIp = request.remote_addr

    if not any(clientIp == user[0] for user in loggedInUsers):
        return jsonify({'error': 'Not logged in'}), 403

    loggedInUsers = [user for user in loggedInUsers if user[0] != clientIp]
    
    return jsonify({'success': 'Logout successful!'}), 200


if __name__ == '__main__':
        # Change this file path if you want to use a different settings file
        settingsData: tuple[str, bool, dict, str, int, bool] = handleSettingsFile('settings.json')

        DATABASE: str = settingsData[0]
        PASSWORD_PROTECTION: bool = settingsData[1]
        LOG_OUT_USERS: bool = settingsData[2]
        LOG_OUT_USERS_AFTER: int = settingsData[3]
        USERS: dict = settingsData[4]
        HOST: str = settingsData[5]
        PORT: int = settingsData[6]
        DEBUG_MODE: bool = settingsData[7]
        
        if PASSWORD_PROTECTION and LOG_OUT_USERS:
            clearLoggedInUsersThread = Thread(target=lambda: clearLoggedInUsers(LOG_OUT_USERS_AFTER), daemon=True)
            clearLoggedInUsersThread.start()

        app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
