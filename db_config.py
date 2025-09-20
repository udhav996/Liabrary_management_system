
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",         # or your MySQL host
            user="root",              # your MySQL username
            password="udhav123", # your MySQL password
            database="library_manager"
        )
        if conn.is_connected():
            print("✅ Connection successful!")
            return conn
    except Error as e:
        print(f"❌ Error: {e}")
        return None
