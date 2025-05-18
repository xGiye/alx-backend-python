# Python Generators for Efficient SQL Data Streaming

This project demonstrates how to use **Python generators** for memory-efficient processing of large datasets from an SQL database using MySQL. Generators are used to stream, batch, and lazily paginate data, as well as to compute aggregate values efficiently without loading the entire dataset into memory.

## Project Structure

```
alx-backend-python/
└── python-generators-0x00/
    ├─ seed.py
    ├─ 0-stream_users.py
    ├─ 1-batch_processing.py
    ├─ 2-lazy_paginate.py
    └─ 3-stream_ages.py
```

---

## seed.py

### Purpose:

- Setup MySQL database `ALX_prodev`
- Create `user_data` table with fields:

  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)

- Populate table from `user_data.csv`

### Key Functions:

- `connect_db()` - Connects to MySQL server
- `create_database(connection)` - Creates `ALX_prodev` if not exists
- `connect_to_prodev()` - Connects to `ALX_prodev` database
- `create_table(connection)` - Creates `user_data` table if not exists
- `insert_data(connection, data)` - Inserts data into table

---

## 0-stream_users.py

### Objective:

Stream rows from `user_data` one by one using a generator.

### Function:

```python
def stream_users():
    # Yields one user row at a time from the user_data table
```

- Uses a generator to fetch each row individually
- Only one loop is allowed

---

## 1-batch_processing.py

### Objective:

Process data in batches from the database and filter users over the age of 25.

### Functions:

```python
def stream_users_in_batches(batch_size):
    # Yields batches of users

def batch_processing(batch_size):
    # Processes each batch to filter users older than 25
```

- Memory-efficient
- Uses generators
- Max 3 loops in entire script

---

## 2-lazy_paginate.py

### Objective:

Simulate paginated fetching using a generator.

### Functions:

```python
def paginate_users(page_size, offset):
    # Returns one page of users starting at offset

def lazy_paginate(page_size):
    # Generator that fetches new pages only when needed
```

- Implements lazy loading using generators
- Only one loop allowed

---

## 3-stream_ages.py

### Objective:

Compute average age of users without loading all data into memory.

### Functions:

```python
def stream_user_ages():
    # Generator yielding one age at a time

def calculate_average_age():
    # Computes average from generator stream
```

- No use of SQL `AVERAGE`
- No more than 2 loops
- Outputs: `Average age of users: <value>`

---

## Usage

1. Run `seed.py` to initialize and populate your database:

   ```bash
   python seed.py
   ```

2. Use each script to demonstrate generator use cases:

   ```bash
   python 0-stream_users.py
   python 1-batch_processing.py
   python 2-lazy_paginate.py
   python 3-stream_ages.py
   ```

---

## Learning Outcomes

- Understand how to use **generators** to handle large datasets
- Learn memory-efficient batch and streaming techniques
- Practice lazy loading and on-demand data access with SQL
- Perform custom aggregation without built-in SQL functions

---

## Technologies Used

- Python 3.x
- MySQL
- `mysql-connector-python`
- CSV for data import

---

## Repository

**GitHub Repo**: `alx-backend-python`

**Directory**: `python-generators-0x00`
