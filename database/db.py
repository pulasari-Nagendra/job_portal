import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        db_host = os.getenv("DB_HOST")

        connection_config = {
            "host": db_host,
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

        # Enable SSL when connecting to Aiven
        if db_host and "aivencloud.com" in db_host:
            connection_config.update({
                "ssl_disabled": False
            })

        connection = mysql.connector.connect(**connection_config)

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None