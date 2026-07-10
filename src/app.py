from flask import Flask, request
import sqlite3
import subprocess
import hashlib

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded credentials
DB_PASSWORD = "P@ssw0rd#2024$ecure!"
API_KEY = "sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop"
SECRET_KEY = "ghp_16C7e42F292c6912E169Taylor0King9"
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# VULNERABILITY 2: SQL Injection
@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Dangerous: direct string formatting in SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return str(cursor.fetchall())

# VULNERABILITY 3: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Dangerous: user input passed directly to shell
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return result.stdout.decode()

# VULNERABILITY 4: Weak cryptography
@app.route('/hash')
def hash_password():
    password = request.args.get('password')
    # Dangerous: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILITY 5: Debug mode enabled
if __name__ == '__main__':
    app.run(debug=True)
