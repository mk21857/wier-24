import db_operations as dbo
import bcrypt
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    # Simple development authentication placeholder
    return username == 'admin' and password == 'admin'

@basic_auth.error_handler
def basic_auth_error(status):
    return jsonify({"success": False, "message": "Wrong credentials!"}), status

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "message": "Object not found!", "error": error}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Server error!", "error": error}), 500

@app.route("/", methods=['GET'])
def home():
    with open('index.html', 'r') as file:
        html_content = file.read()
        print(html_content)
    return html_content

@app.route("/test_connection" , methods=['GET'])
@basic_auth.login_required
def test_connection():
    retVal = dbo.test_db_connection()
    return jsonify(retVal)

@app.route("/execute_script/<string:script_name>", methods=['POST'])
@basic_auth.login_required
def execute_script(script_name):
    retVal = dbo.execute_sql_script(script_name)
    return jsonify(retVal)

@app.route("/drop_db", methods=['POST'])
@basic_auth.login_required
def drop_db():
    # retVal = dbo.drop_database()
    # return jsonify(retVal)
    return jsonify({"success": False, "error": "This operation is disabled! Enable it by commenting out the code."})

@app.route("/get_tables", methods=['GET'])
@basic_auth.login_required
def get_tables():
    tables = dbo.get_all_tables()
    return jsonify(tables)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')