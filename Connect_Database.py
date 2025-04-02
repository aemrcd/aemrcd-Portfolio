from mysql.connector import Error
import mysql.connector

def connect_to_database():
    try:
        # XAMMPP MySQL connection
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",  
            password="",  
            port=3306

        # UBUNTU MySQL connection
        )

        if connection.is_connected():
            print("Connection to MySQL database was successful!")
            # You can add additional code here to interact with the database

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")

# Call the function to test the connection
connect_to_database()