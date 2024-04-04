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
        return {"success": True, "message":
                "Connection to database successful!"}
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
                return {"success": True, "message":
                        f"Script '{script_file_path}' executed successfully!"}
        else:
            return {"success": False, "error":
                    f"Script '{script_file_path}' does not exist."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def drop_database():
    try:
        conn = get_database_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS"
                    f" {os.environ.get('CLOUD_SQL_DATABASE')}")
        cur.close()
        conn.close()
        return {"success": True, "message": f"Database"
                f" '{os.environ.get('CLOUD_SQL_DATABASE')}'"
                f" dropped successfully!"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_all_tables():
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT table_name FROM information_schema.tables"
                    f" WHERE table_schema ="
                    f" '{os.environ.get('CLOUD_SQL_DATABASE')}'")
        tables = cur.fetchall()
        all_tables = [table[0] for table in tables]
        return {"success": True,
                "message": f"Successfully retrieved all"
                f" tables from '{os.environ.get('CLOUD_SQL_DATABASE')}'.",
                "data": all_tables}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_frontier_pages(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, url FROM crawldb.page "
            "WHERE page_type_code = 'FRONTIER' "
            "ORDER BY id"
        )
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        print("Error while fetching frontier pages:", e)
        return []


def insert_site(conn, domain, robots_content, sitemap_content):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO crawldb.site "
            "(domain, robots_content, sitemap_content) "
            "VALUES (%s, %s, %s) RETURNING id",
            (domain, robots_content, sitemap_content)
        )
        site_id = cursor.fetchone()[0]
        conn.commit()
        print("Site data inserted successfully with ID:", site_id)
        return site_id
    except Exception as e:
        print("Error while inserting site data:", e)
        conn.rollback()
        return None
    finally:
        if cursor is not None:
            cursor.close()


def insert_image(conn, url, filename, content_type, accessed_time):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM crawldb.page WHERE url = %s", (url,)
        )
        page_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO crawldb.image "
            "(page_id, filename, content_type, accessed_time) "
            "VALUES (%s, %s, %s, %s)",
            (page_id, filename, content_type, accessed_time)
        )
        conn.commit()
        print("Image data inserted successfully.")
    except Exception as e:
        print("Error while inserting image data:", e)
        conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()


def insert_page_into_frontier(conn, domain, url, page_type='FRONTIER',
                              from_page=None):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM crawldb.site"
                       " WHERE domain = %s", (domain,))
        site_id = cursor.fetchone()
        if site_id is None:
            # Create a new site entry
            # site_id = insert_site(conn, domain, None, None, None)
            pass
        # else:
            # site_id = site_id[0]

        print('site_id', site_id)
        cursor.execute(
            "INSERT INTO crawldb.page (site_id, url, page_type_code) "
            "VALUES (%s, %s, %s) RETURNING id",
            (0, url, page_type)
        )
        to_page_id_result = cursor.fetchone()

        if from_page is not None and to_page_id_result is not None:
            to_page_id = to_page_id_result[0]
            cursor.execute("SELECT id FROM crawldb.page "
                           "WHERE url = %s", (from_page,))
            from_page_id_result = cursor.fetchone()
            if from_page_id_result is not None:
                from_page_id = from_page_id_result[0]
                cursor.execute(
                    "INSERT INTO crawldb.crawl_links (from_page, to_page) ",
                    "VALUES (%s, %s)",
                    (from_page_id, to_page_id)
                )
        conn.commit()
        print("Page inserted into frontier successfully.")
    except Exception as e:
        print("Error while inserting page into frontier:", e)
        conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()


def get_frontier_length(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM crawldb.page ",
            "WHERE page_type_code = 'FRONTIER'"
        )
        length = cursor.fetchone()[0]
        print("Frontier length:", length)
        return length
    except Exception as e:
        print("Error while fetching frontier length:", e)
        return 0
    finally:
        if cursor is not None:
            cursor.close()


def update_page_data(conn, url, page_type):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE crawldb.page SET page_type_code = %s ",
            "WHERE url = %s",
            (page_type, url)
        )
        conn.commit()
        print("Page data updated successfully.")
    except Exception as e:
        print("Error while updating page data:", e)
        conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()


def get_page(conn, url):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, site_id, url, page_type_code ",
            "FROM crawldb.page WHERE url = %s",
            (url,)
        )
        return cursor.fetchone()
    except Exception as e:
        print("Error while fetching page data:", e)
        return None
    finally:
        if cursor is not None:
            cursor.close()


def get_site(conn, domain):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, domain, robots_content, sitemap_content, ip_address ",
            "FROM crawldb.site WHERE domain = %s",
            (domain,)
        )
        return cursor.fetchone()
    except Exception as e:
        print("Error while fetching site data:", e)
        return None
    finally:
        if cursor is not None:
            cursor.close()

