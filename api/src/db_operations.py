import os
import psycopg2
import threading

lock = threading.Lock()

def get_database_connection():
    host = os.environ.get("CLOUD_SQL_HOST")
    port = int(os.environ.get("CLOUD_SQL_PORT"))
    database = os.environ.get("CLOUD_SQL_DATABASE")
    user = os.environ.get("CLOUD_SQL_USER")
    password = os.environ.get("CLOUD_SQL_PASSWORD")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Connected to Cloud SQL database!")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e

def test_db_connection():
    try:
        conn = get_database_connection()
        conn.close()
        return {"success": True, "message": "Connection to database successful!"}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

def execute_sql_script(script_file_path):
    try:
        script_path = f'/app/init-scripts/{script_file_path}'
        if os.path.exists(script_path):
            with open(script_path, 'r') as script_file:
                conn = get_database_connection()
                cur = conn.cursor()
                cur.execute(script_file.read())
                conn.commit()
                cur.close()
                conn.close()
                return {"success": True, "message": f"Script '{script_file_path}' executed successfully!"}
        else:
            return {"success": False, "error": f"Script '{script_file_path}' does not exist."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def drop_database():
    try:
        conn = get_database_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {os.environ.get('CLOUD_SQL_DATABASE')}")
        cur.close()
        conn.close()
        return {"success": True, "message": f"Database '{os.environ.get('CLOUD_SQL_DATABASE')}' dropped successfully!"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_tables():
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{os.environ.get('CLOUD_SQL_DATABASE')}'")
        tables = cur.fetchall()
        all_tables = [table[0] for table in tables]
        return {"success": True, "message": f"Successfully retrieved all tables from '{os.environ.get('CLOUD_SQL_DATABASE')}'.", "data": all_tables}
    except Exception as e:
        return {"success": False, "error": str(e)}