import logging
import sqlite3
from langchain_community.utilities.sql_database import SQLDatabase
from llm import llm
from langchain.chains import create_sql_query_chain
from clean import clean_sql_query



DB_PATH = "my_database.db" 
db = SQLDatabase.from_uri( f"sqlite:///{DB_PATH}") 

connection = sqlite3.connect(DB_PATH, check_same_thread=False) 

def nlsql(query):
    generate_query = create_sql_query_chain(llm, db)
    query = generate_query.invoke({"question": query})
    query =clean_sql_query(query)
    return query

def execute_sql(sql):
    """Execute an SQL query and return results or an error message."""
    sql=nlsql(sql)
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


