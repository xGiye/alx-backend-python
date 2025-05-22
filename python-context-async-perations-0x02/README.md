# python-context-async-perations-0x02

This repository contains Python scripts demonstrating the use of context managers and asynchronous operations for database interactions using both `sqlite3` and `aiosqlite`.

## Project Overview

The goal is to implement safe and efficient database operations by leveraging:

- Custom class-based context managers
- Reusable query execution logic
- Asynchronous programming for concurrent database queries

---

## Tasks Summary

### 0. Custom Database Connection Context Manager

**File**: [`0-databaseconnection.py` ](0-databaseconnection.py)

**Objective**:  
Implement a class-based context manager `DatabaseConnection` to automatically manage opening and closing of SQLite database connections.

**Features**:

- Uses `__enter__()` and `__exit__()` methods
- Ensures safe resource cleanup
- Example included: fetch all users from the `users` table

---

### 1. Reusable Query Context Manager

**File**: [`1-execute.py`](1-execute.py)

**Objective**:  
Create a reusable context manager `ExecuteQuery` that takes a SQL query and its parameters, executes it, and returns the result.

**Features**:

- Executes parameterized queries securely
- Automatically manages both connection and cursor cleanup
- Example included: fetch users older than 25

---

### 2. Concurrent Asynchronous Database Queries

**File**: [`3-concurrent.py` ](3-concurrent.py)

**Objective**:  
Use `aiosqlite` and `asyncio.gather()` to run multiple queries concurrently.

**Features**:

- Asynchronous query functions: `async_fetch_users()` and `async_fetch_older_users()`
- Uses `asyncio.run()` to execute concurrent operations
- Efficiently fetches all users and users older than 40 in parallel

---

## Requirements

- Python 3.7+
- `aiosqlite` (Install via pip)

```bash
pip install aiosqlite
```
