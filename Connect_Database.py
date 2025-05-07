import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            # host="localhost",
            # user="root",
            # password="",
            # port=3306,
            # database="mycontactdb"

            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=3306
        )
        if connection.is_connected():
            print("✅ Connection successful!")
            return connection
    except Error as e:
        print(f"❌ Error: {e}")
        return None
    

# connect_to_database()




# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     emailhash VARCHAR(64) NOT NULL UNIQUE,
#     emaildomain VARCHAR(255) NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     created_on DATE DEFAULT (CURRENT_DATE)
# ); 