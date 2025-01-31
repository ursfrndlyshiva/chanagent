import pymysql
from dotenv import load_dotenv
import os
from langchain_community.utilities.sql_database import SQLDatabase


load_dotenv()


host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')


connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)


