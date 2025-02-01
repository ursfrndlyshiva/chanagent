import logging
import sqlite3

# Define the database path and establish a connection
DB_PATH = "my_database.db"  # Replace with your database file path
connection = sqlite3.connect(DB_PATH, check_same_thread=False)  # Creating SQLite connection

def execute_sql(sql):
    """Execute an SQL query and return results or an error message."""
    cursor = None  # Initialize cursor as None to prevent errors in the finally block
    try:
        with connection:  # Ensures automatic commit & rollback
            cursor = connection.cursor()  # Create the cursor inside the context manager
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                return "No data available for this query."

            return results

    except sqlite3.Error as e:  # Handle SQLite errors
        logging.error(f"SQL Error: {str(e)}")
        return f"Database error: {str(e)}"

    except Exception as e:  # Handle unexpected errors
        logging.error(f"Unexpected Error: {str(e)}")
        return "An unexpected error occurred while executing the query."

    finally:
        if cursor:
            cursor.close()  # Ensure cursor is closed after execution


