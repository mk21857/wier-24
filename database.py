import psycopg2


def connect_to_database():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432",
            database="postgres"  # replace with your database name
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


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
        # Fetch all the rows and return them
        rows = cursor.fetchall()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error executing query:", error)


    """if __name__ == "__main__":
        # Connect to the database
        connection = connect_to_database()

        # Example query
        query = "SELECT * FROM crawldb.data_type;"
        
    # Execute query
        records = execute_query(connection, query)
        if records:
            print("Values in crawldb.data_type table:")
            for row in records:
                print(row)
        
        # Close connection
        close_connection(connection)"""


def get_domain_ips(conn):
    cursor = None
    domains = []
    ips = []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ip, domain FROM crawldb.site")
        result = cursor.fetchall()

        if result is not None:
            for row in result:
                domains.append(row[0])
                ips.append(row[1])

        return domains, ips

    except Exception as e:
        print("Error in get_domain_ips:", e)
        return [], []

    finally:
        if cursor is not None:
            cursor.close()


