import os
import psycopg2
import threading

lock = threading.Lock()


def get_database_connection():
    host = os.environ.get("POSTGRES_HOST")
    port = int(os.environ.get("POSTGRES_PORT"))
    database = os.environ.get("POSTGRES_DB")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")

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
        script_path = f'/app/sql_scripts/{script_file_path}'
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


def get_frontier_pages():
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, url FROM crawldb.page "
            "WHERE page_type_code = 'FRONTIER' "
            "ORDER BY id"
        )
        conn.commit()
        res = cur.fetchall()
        return {"success": True,
                "message": "Frontier pages fetched successfully!",
                "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}


def insert_site(domain, robots_content, sitemap_content):
    try:
        conn = get_database_connection()
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


def insert_image(url, filename, content_type, accessed_time):
    try:
        conn = get_database_connection()
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


def insert_page_into_frontier(
        domain,
        url,
        robots_content=None,
        sitemap_content=None,
        from_page=None):
    try:
        page_type_code = 'FRONTIER'
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM crawldb.site"
                       " WHERE domain = %s", (domain,))
        site_id = cursor.fetchone()
        if site_id is None:
            site_id = insert_site(domain, robots_content, sitemap_content)
        else:
            site_id = site_id[0]

        cursor.execute(
            "INSERT INTO crawldb.page (site_id, url, page_type_code) "
            "VALUES (%s, %s, %s) RETURNING id",
            (site_id, url, page_type_code)
        )
        page_id = cursor.fetchone()[0]

        # Add LINKS
        if from_page is not None:
            cursor.execute(
                "SELECT id FROM crawldb.page WHERE url = %s", (from_page,)
            )
            from_page_id = cursor.fetchone()

            if from_page_id is not None:
                cursor.execute(
                    "INSERT INTO crawldb.link (from_page, to_page) "
                    "VALUES (%s, %s)",
                    (from_page_id[0], page_id)
                )
        else:
            cursor.execute(
                "INSERT INTO crawldb.link (from_page, to_page) "
                "VALUES (%s, %s)",
                (page_id, page_id)
            )

        conn.commit()
        print("Page inserted into frontier successfully.")

        return {"success": True, "message": "Inserted page into frontier.",
                "data": page_id}
    except Exception as e:
        print("Error while inserting page into frontier:", e)
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()


def get_frontier_length():
    try:
        conn = get_database_connection()
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


def update_page_data(url, page_type_code, html_content, http_status_code,
                     accessed_time, data_type_code=None, robots_content=None,
                     sitemap_content=None, hashed_content=None):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        #cursor.execute("SELECT site_id FROM crawldb.page WHERE url = %s AND robots_content NOT null", (url,))
        cursor.execute("SELECT DISTINCT s.id FROM crawldb.site s "
                       "INNER JOIN crawldb.page p ON p.site_id = s.id "
                       "WHERE p.url = %s AND s.robots_content is null",
                       (url, ))
        site_id = cursor.fetchone()
        print("Site ID:", site_id)
        if site_id is not None:
            site_id = site_id[0]
            print("Site ID:", site_id)
        #if site_id is not None and robots_content is not None and sitemap_content is not None:
            site_id = update_site(site_id, robots_content, sitemap_content)
        #else:
        #    site_id = site_id[0]
        cursor.execute(
            "SELECT id FROM crawldb.page WHERE hashed_content = %s", (hashed_content,)
        )
        is_duplicate = cursor.fetchone()

        if (page_type_code == 'HTML'):
            cursor.execute(
                "UPDATE crawldb.page "
                "SET page_type_code = %s, html_content = %s, "
                "http_status_code = %s, "
                "accessed_time = %s, "
                "hashed_content = %s "
                "WHERE url = %s",
                (page_type_code, html_content, http_status_code, accessed_time, 
                 hashed_content, url)
            )
        elif (page_type_code == 'BINARY'):
            cursor.execute(
                "UPDATE crawldb.page "
                "SET page_type_code = %s, "
                "http_status_code = %s, "
                "accessed_time = %s "
                "WHERE url = %s",
                (page_type_code, http_status_code, accessed_time,
                 url)
            )
            cursor.execute(
                "INSERT INTO crawldb.page_data "
                "(page_id, data_type_code) "
                "VALUES ((SELECT id FROM crawldb.page WHERE url = %s),"
                " %s)",
                (url, data_type_code)
            )
        elif (page_type_code == 'ERROR'):
            cursor.execute(
                "UPDATE crawldb.page "
                "SET page_type_code = %s, html_content = %s, "
                "http_status_code = %s, "
                "accessed_time = %s, "
                "hashed_content = %s "
                "WHERE url = %s",
                (page_type_code, html_content, http_status_code, accessed_time, 
                 hashed_content, url)
            ) 

        
        if is_duplicate is not None:
            page_type_code = 'DUPLICATE'

            cursor.execute(
                "SELECT id FROM crawldb.page WHERE url = %s", (url,)
            )
            
            to_id = cursor.fetchone()
            if to_id is not None:
                cursor.execute(
                    "INSERT INTO crawldb.link (to_page, from_page) "
                    "VALUES (%s, %s) ",
                    (is_duplicate[0], to_id[0])
                )
            cursor.execute(
                "UPDATE crawldb.page "
                "SET page_type_code = %s, "
                "http_status_code = %s, "
                "accessed_time = %s "
                "WHERE url = %s",
                (page_type_code, http_status_code, accessed_time, url)
            )
        conn.commit()
        return {"success": True, "message": "Page data updated successfully!"}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()


def update_site(id, robots_content, sitemap_content):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE crawldb.site "
            "SET robots_content = %s, sitemap_content = %s "
            "WHERE id = %s",
            (robots_content, sitemap_content, id)
        )
        conn.commit()
        response = {"success": True, "message": "Site data updated successfully!"}
        print(response)
        return response
    except Exception as e:
        conn.rollback()
        response = {"success": False, "error": str(e)}
        return response
    finally:
        if cursor is not None:
            cursor.close()


def get_page(url):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, site_id, url, page_type_code, html_content "
            "FROM crawldb.page WHERE url = %s",
            (url,)
        )
        retVal = cursor.fetchone()
        return {"success": True, "message": "Page fetched successfully!", "data": retVal}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()


def get_site(domain):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, domain, robots_content, sitemap_content ",
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


def get_hashed_content():
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hashed_content FROM crawldb.page WHERE hashed_content is not null"
        )
        retVal = cursor.fetchall()
        print("Hash", retVal)
        return {"success": True, "message": "Hash values fetched successfully!", "data": retVal}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()
