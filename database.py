import sqlite3

# Define the database file
DB_PATH = "my_database.db"

# Create a persistent connection
connection = sqlite3.connect(DB_PATH, check_same_thread=False)  # Allows sharing connection across threads
