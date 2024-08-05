import mysql.connector

def test_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="695379779",
            user="admin",
            password="meico1234",
            database="meico"
        )
        if conn.is_connected():
            print("Connected successfully")
        else:
            print("Failed to connect")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Connection closed")

if __name__ == "__main__":
    test_connection()



