import os
import psycopg2
import threading

lock = threading.Lock()

def get_database_connection():
    host = "cloudsql-proxy"
    port = 5432
    database = "crawldb"
    user = "postgres"
    password = "pajki-wier24"

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

def execute_sql_script():
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        with open('/app/init-scripts/database.sql', 'r') as script_file:
            cur.execute(script_file.read())

        conn.commit()
        cur.close()
        conn.close()
        print("SQL script executed successfully!")
    except Exception as e:
        print(f"Error executing SQL script: {e}")
        raise e

def test_db_connection():
    try:
        conn = get_database_connection()
        conn.close()
        return {"success": True}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

def get_all_tables():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    all_tables = [table[0] for table in tables]
    return all_tables

def reset_db_values():
    conn = get_database_connection()
    conn.autocommit = True
    
    cur = conn.cursor()
    cur.execute("UPDATE showcase.counters SET value = 0")
    
    cur.close()
    conn.close()
    
def print_db_values():
    print("Getting connection")
    conn = get_database_connection()
    print("Got connection")
    conn.autocommit = True

    retVal = []
    print("\nValues in the database:")
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawldb.site")
    rows = cur.fetchall()
    for row in rows:
        site_id = row
        print(f"\tSite ID: {site_id}")
        retVal.append({'site_id': site_id})
    cur.close()
    conn.close()
    return retVal


def increase_db_values(counter_id):
    conn = get_database_connection()
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
    conn = get_database_connection()
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