import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries with date and time
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{current_time}] Executing query: {query}")
        else:
            print(f"[{current_time}] No SQL query found to execute.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")