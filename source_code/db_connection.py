import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def get_db_connection():
    load_dotenv()  # Loads variables from .env
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
    return None
