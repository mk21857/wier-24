import psycopg2


def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432",
            database="postgres"
        )
        print("Connected to the database successfully.")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None


def close_connection(connection):
    if connection:
        connection.close()
        print("Connection to the database closed.")


def execute_query(connection, query, parameters=None):
    try:
        cursor = connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error executing query:", error)


def get_frontier_pages(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, url FROM crawldb.page ",
            "WHERE page_type_code = 'FRONTIER' ",
            "ORDER BY id"
        )
        return cursor.fetchall()
    except Exception as e:
        print("Error while fetching frontier pages:", e)
        return []


def insert_site(conn, domain, robots_content, sitemap_content, ip_address):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO crawldb.site ",
            "(domain, robots_content, sitemap_content, ip) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (domain, robots_content, sitemap_content, ip_address)
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
            "INSERT INTO crawldb.image ",
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

        cursor.execute("SELECT id FROM crawldb.site",
                       " WHERE domain = %s", (domain,))
        site_id = cursor.fetchone()
        if site_id is None:
            print("No domain stored with this url:", url)
            return

        cursor.execute(
            "INSERT INTO crawldb.page (site_id, url, page_type_code) "
            "VALUES (%s, %s, %s) RETURNING id",
            (site_id[0], url, page_type)
        )
        to_page_id_result = cursor.fetchone()

        if from_page is not None and to_page_id_result is not None:
            to_page_id = to_page_id_result[0]
            cursor.execute("SELECT id FROM crawldb.page ",
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


def get_frontier_length():
    try:
        conn = connect_to_database()
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
        close_connection(conn)


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


if __name__ == "__main__":
    connection = connect_to_database()
    # execute_query(connection, "INSERT INTO crawldb.data_type (code)"
    #              " VALUES ('IMG');")
    query = "SELECT * FROM crawldb.data_type;"
    records = execute_query(connection, query)
    if records:
        print("Values in crawldb.data_type table:")
        for row in records:
            print(row)
    close_connection(connection)
