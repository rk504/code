import sqlite3

# Replace with your actual database file path
database = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.db'  # e.g., 'data/doordash.db'

try:
    conn = sqlite3.connect(database)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {str(e)}") 