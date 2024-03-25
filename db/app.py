#--- Database operations ---#

import threading
import psycopg2
import bcrypt

lock = threading.Lock()

db_host = "db"
db_name = "user"
db_user = "user"
db_password = "SecretPassword"

def reset_db_values():
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password)
    conn.autocommit = True
    
    cur = conn.cursor()
    cur.execute("UPDATE showcase.counters SET value = 0")
    
    cur.close()
    conn.close()
    
def print_db_values():
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password)
    conn.autocommit = True

    retVal = []
    print("\nValues in the database:")
    cur = conn.cursor()
    cur.execute("SELECT counter_id, value FROM showcase.counters ORDER BY counter_id")
    for counter_id, value in cur.fetchall():
        print(f"\tCounter id: {counter_id}, value: {value}")
        retVal.append({counter_id: value})
    cur.close()
    conn.close()
    return retVal

def increase_db_values(counter_id):
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password)
    conn.autocommit = True
    
    cur = conn.cursor()
    cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
                (counter_id,))
    value = cur.fetchone()[0]
    cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
                (value+1, counter_id))
    cur.close()
    conn.close()
    
def increase_db_values_locking(counter_id):
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password)
    conn.autocommit = True

    with lock:
        cur = conn.cursor()
        cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
                    (counter_id,))
        value = cur.fetchone()[0]
        cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
                    (value+1, counter_id))
        cur.close()
    conn.close()

#--- Flask server ---#

from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

#--- Authentication ---#

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    try:
        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Execute a parameterized query to fetch user details by username
        cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        # If user exists and provided password matches hashed database password, return True
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return True

    except Exception as e:
        print("Error:", e)
    finally:
        # Close cursor and connection
        cur.close()
        conn.close()
    
    return False

@basic_auth.error_handler
def basic_auth_error(status):
    return jsonify({"success": False, "message": "Wrong credentials!"}), status

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "message": "Object not found!"}), 404

@app.errorhandler(500)
def internal_error(error):
    # rollback db if using transactions
    return jsonify({"success": False, "message": "Server error!"}), 500

#--- Routes ---#

@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/db/reset', methods=['POST'])
@basic_auth.login_required
def fl_restart():
    reset_db_values()
    return jsonify({"success": True})

@app.route('/db/get_values', methods=['GET'])
# @basic_auth.login_required
def fl_get_values():
    retVal = print_db_values()
    return jsonify(retVal)
    
@app.route('/db/increase/<int:id>', methods=['POST'])
@basic_auth.login_required
def fl_inc_vals(id):
    increase_db_values(id)
    return jsonify({"success": True})

@app.route('/db/increase_locking/<int:id>', methods=['POST'])
@basic_auth.login_required
def fl_inc_vals_lock(id):
    increase_db_values_locking(id)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(ssl_context='adhoc')