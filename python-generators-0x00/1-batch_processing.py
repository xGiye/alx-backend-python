#!/usr/bin/python3

import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database."""
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
        
        batch = []
        for row in cursor:  # 1st loop
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:  # Yield the last partial batch
            yield batch

    except mysql.connector.Error as e:
        print(f"Error streaming users in batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """Processes batches and yields users over age 25."""
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        filtered_batch = [user for user in batch if user.get("age", 0) > 25]  # 3rd loop (list comprehension)
        if filtered_batch:
            yield filtered_batch
