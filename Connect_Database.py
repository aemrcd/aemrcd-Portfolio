import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            # host="localhost",
            # user="root",
            # password="",
            # port=3306,

            host="10.2.3.127",
            user="AEROL",
            database="myContact",
            password="1234"

        )
        if connection.is_connected():
            print("✅ Connection successful!")
            return connection
    except Error as e:
        print(f"❌ Error: {e}")
        return None

connect_to_database()

