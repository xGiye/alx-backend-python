# Python Decorators – Database Operation Enhancements

This project demonstrates the practical use of **Python decorators** to enhance database interactions using `sqlite3`. The tasks simulate real-world challenges that professional developers may face when working with database-driven applications.

## Project Description

This project focuses on mastering Python decorators to streamline and strengthen database operations. You'll learn to:

- Automate repetitive DB tasks,
- Improve transaction safety,
- Increase performance through caching,
- Handle transient DB failures gracefully,
- And log queries for better observability.

Each task builds upon the last, culminating in a set of reusable, robust decorator tools that can be applied to any SQLite-based Python application.

---

## Learning Objectives

- **Understand and use Python decorators** to write reusable and clean code.
- **Automate** connection handling and transaction management.
- **Add resilience** with retry mechanisms for transient errors.
- **Boost performance** by caching SQL query results.
- **Apply best practices** for scalable Python applications.

---

## Requirements

- Python 3.8+
- SQLite3 installed and a `users.db` database with a `users` table.
- Git and GitHub familiarity
- Knowledge of Python decorators and database concepts

---

## Tasks & Solutions

### `0-log_queries.py` - **Log Database Queries**

**Objective:** Implement `log_queries` decorator that logs every SQL query before execution.

**Solution:** [Log queries]('./0-log_queries.py')

### `1-with_db_connection.py` - **Database Connection Decorator**

**Objective**: Implement with_db_connection to automatically open and close SQLite connections.

**Solution:** [Database Connection Decorator]('./1-with_db_connection.py')

### `2-transactional.py` - **Transaction Management Decorator**

**Objective**: Create @transactional to manage DB transactions (commit on success, rollback on error).

**Solution:** [Transaction Management Decorator]('./2-transactional.py')

### `3-retry_on_failure.py` - **Retry on Failure Decorator**

**Objective:** Implement retry_on_failure(retries=3, delay=2) decorator to handle transient errors.

**Solution:** [Retry on Failure Decorator]('./3-retry_on_failure.py')

### `4-cache_query.py` - **Query Result Caching**

**Objective:** Implement cache_query decorator to avoid redundant DB calls by caching results.

**Solution:** [Query Result Caching]('./4-cache_query.py')
