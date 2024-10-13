import os
import sqlite3
import logging

# Set up logging
logging.basicConfig(
    filename='application.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_to_db():
    """Establishes a connection to the SQLite database 'database.db'."""
    try:
        conn = sqlite3.connect('database.db')
        logging.info("Database connection established successfully.")
        return conn
    except sqlite3.Error as e:
        logging.error("Database connection failed: %s", e)
        raise e

def create_user_table():
    """Creates the 'users' table in the database if it does not already exist."""
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                last_read_date DATE,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0
            )
        ''')
        logging.info("Table 'users' created or already exists.")
        conn.commit()
    except sqlite3.Error as e:
        logging.error("Error creating 'users' table: %s", e)
        raise e
    finally:
        conn.close()

def print_all_users():
    """Prints all records from the 'users' table."""
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        if users:
            for user in users:
                print(user)
        else:
            print("No users found in the database.")
    except sqlite3.Error as e:
        logging.error("Error accessing 'users' table: %s", e)
    finally:
        conn.close()

# Execute the functions
create_user_table()  # Ensure the table exists
print_all_users()    # Print all users
