import db_operations as dbo
import bcrypt
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    conn = dbo.get_database_connection()
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user_data = cur.fetchone()

    if user_data:
        hashed_password = user_data[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return username

    cur.close()
    conn.close()
    return None

@basic_auth.error_handler
def basic_auth_error(status):
    return jsonify({"success": False, "message": "Wrong credentials!"}), status

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "message": "Object not found!"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Server error!"}), 500

@app.route("/")
def hello_world():
    retVal = dbo.test_db_connection()
    print(retVal)
    return jsonify(retVal)

@app.route("/create_tables")
def create_tables():
    dbo.execute_sql_script()
    return jsonify({"success": True})

@app.route("/tables")
def get_tables():
    tables = dbo.get_all_tables()
    return jsonify(tables)

@app.route('/db/reset', methods=['POST'])
@basic_auth.login_required
def fl_restart():
    dbo.reset_db_values()
    return jsonify({"success": True})

@app.route('/db/get_values', methods=['GET'])
# @basic_auth.login_required
def fl_get_values():
    retVal = dbo.print_db_values()
    return jsonify(retVal)
    
@app.route('/db/increase/<int:id>', methods=['POST'])
@basic_auth.login_required
def fl_inc_vals(id):
    dbo.increase_db_values(id)
    return jsonify({"success": True})

@app.route('/db/increase_locking/<int:id>', methods=['POST'])
@basic_auth.login_required
def fl_inc_vals_lock(id):
    dbo.increase_db_values_locking(id)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(ssl_context='adhoc')