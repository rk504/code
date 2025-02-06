import pandas as pd
import sqlite3

# Define the path to your CSV file and the SQLite database
csv_file_path = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.csv'  # Path to your CSV file
database_path = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.db'  # Path to your SQLite database

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(csv_file_path)
    print("CSV file read successfully!")
except FileNotFoundError:
    print(f"Error: The file at {csv_file_path} was not found.")
    exit()
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(database_path)

# Write the DataFrame to the SQLite database
try:
    df.to_sql('delivery_data', conn, if_exists='replace', index=False)
    print("Data successfully imported to SQLite database!")
except Exception as e:
    print(f"Error importing data to database: {e}")
finally:
    conn.close() 