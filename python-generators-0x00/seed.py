import csv
import uuid
import mysql.connector
from mysql.connector import Error


def connect_db():
    """Connects to MySQL server (no DB selected)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates ALX_prodev DB if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates user_data table."""
    try:
        cursor = connection.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data from user_data.csv into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                insert_query = """
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
