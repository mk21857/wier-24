import db_operations as dbo
# import bcrypt
from flask import Flask, jsonify, request
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
    return jsonify({"success": False, "message": "Object not found!",
                    "error": error}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Server error!",
                    "error": error}), 500


@app.route("/", methods=['GET'])
def home():
    with open('index.html', 'r') as file:
        html_content = file.read()
        print(html_content)
    return html_content


@app.route("/test_connection", methods=['GET'])
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
    retVal = dbo.drop_database()
    return jsonify(retVal)
    # return jsonify({"success": False, "error": "This operation is disabled!"
    #                 " Enable it by commenting out the code."})


@app.route("/get_tables", methods=['GET'])
@basic_auth.login_required
def get_tables():
    tables = dbo.get_all_tables()
    return jsonify(tables)


@app.route("/get_frontier_pages", methods=['GET'])
@basic_auth.login_required
def get_frontier_pages():
    retVal = dbo.get_frontier_pages()
    return jsonify(retVal)


@app.route("/insert_site", methods=['POST'])
@basic_auth.login_required
def insert_site():
    data = request.get_json()
    site_id = dbo.insert_site(data.get("domain"), data.get("robots_content"), data.get("sitemap_content"))
    return jsonify("data", site_id)


@app.route("/insert_image", methods=['POST'])
@basic_auth.login_required
def insert_image():
    data = request.get_json()
    retVal = dbo.insert_image(data.get("image"))
    return jsonify(retVal)

@app.route("/insert_page_data/<string:page_id>", methods=['POST'])
@basic_auth.login_required
def insert_page_data(page_id):
    data = request.get_json()
    retVal = dbo.insert_image(page_id, data.get("image"))
    return jsonify(retVal)

@app.route("/insert_page_into_frontier", methods=['POST'])
@basic_auth.login_required
def insert_page_into_frontier():
    data = request.get_json()
    retVal = dbo.insert_page_into_frontier(
        domain = data.get("domain"),
        url = data.get("url"),
        # html_content = data.get("html_content"),
        # http_status_code = data.get("http_status_code"),
        # accessed_time = data.get("accessed_time"),
        # from_page = data.get("from_page"),
        # robots_content = data.get("robots_content"),
        # sitemap_content = data.get("sitemap_content"),
    )
    return jsonify(retVal)


@app.route("/get_frontier_length", methods=['GET'])
@basic_auth.login_required
def get_frontier_length():
    length = dbo.get_frontier_length()
    return jsonify("Frontier length:", length)


@app.route("/update_page_data", methods=['POST'])
@basic_auth.login_required
def update_page_data():
    data = request.get_json()
    retVal = dbo.update_page_data(
        # domain = data.get("domain"),
        url = data.get("url"),
        html_content = data.get("html_content"),
        http_status_code = data.get("http_status_code"),
        accessed_time = data.get("accessed_time"),
        page_type_code = data.get("page_type_code"),
        # from_page = data.get("from_page"),
        # robots_content = data.get("robots_content"),
        # sitemap_content = data.get("sitemap_content"),
    ) # Dodaj .get("karkoli_rabiš") za vsak parameter
    return jsonify(retVal)


@app.route("/get_page", methods=['GET'])
@basic_auth.login_required
def get_page():
    data = request.get_json()
    retVal = dbo.get_page(data.get("url"))
    return jsonify(retVal)


@app.route("/get_site", methods=['GET'])
@basic_auth.login_required
def get_site():
    cursor = dbo.get_site()
    return jsonify(cursor)

@app.route("/get_hashed_content", methods=['GET'])
@basic_auth.login_required
def get_hashed_content():
    retVal = dbo.get_hashed_content()
    return jsonify(retVal)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
