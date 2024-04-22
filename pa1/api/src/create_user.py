import bcrypt
import psycopg2

# Function to securely create a user in the database
def create_user(username, password):
    try:
        # Connect to the database
        conn = psycopg2.connect(host="db", dbname="user", user="user", password="SecretPassword")
        cur = conn.cursor()

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user data into the database
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        print("User created successfully")

        # Close cursor and connection
        cur.close()
        conn.close()

        return {"success": True, "message": "User created successfully"}
    except Exception as e:
        print("Error:", e)
        return {"success": False, "message": str(e)}