#!/usr/bin/python3
    
import mysql.connector

def stream_users():
    """Stream rows from user_data table one by one using a generator."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, email, age FROM user_data")
        for row in cursor:
            yield row
    except mysql.connector.Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

