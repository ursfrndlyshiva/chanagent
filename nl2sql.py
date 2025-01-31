from langchain.chains import create_sql_query_chain
from clean import clean_sql_query
from database import connection
from llm import llm
import logging
import pymysql



  

def execute_sql(sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results: 
                return "No data available for this query."

            return results

    except pymysql.MySQLError as e:  
        logging.error(f"SQL Error: {str(e)}")
        return f"Database error: {str(e)}"

    except Exception as e: 
        logging.error(f"Unexpected Error: {str(e)}")
        return "An unexpected error occurred while executing the query."
