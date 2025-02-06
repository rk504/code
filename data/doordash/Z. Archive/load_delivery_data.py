import pandas as pd
import pyodbc
import sqlalchemy
from sqlalchemy import create_engine
import urllib

# Database connection parameters
server = 'YOUR_SERVER_NAME'  # e.g., 'localhost' or server IP
database = 'YOUR_DATABASE_NAME'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Create connection string
params = urllib.parse.quote_plus(
    'DRIVER={SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Create engine
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

# Read CSV file
df = pd.read_csv('Drive_Case_Study_Data_2024_(2).csv')

# Convert boolean columns
boolean_columns = ['is_first_delivery', 'asap', 'fraudulent', 'manually_assigned', 'was_batched']
for col in boolean_columns:
    df[col] = df[col].astype(int)  # Convert True/False to 1/0

# Convert timestamp columns
timestamp_columns = [
    'created_at', 'quoted_delivery_time', 'estimated_delivery_time',
    'actual_pickup_time', 'actual_delivery_time', 'dasher_assigned_time',
    'dasher_confirmed_time', 'dasher_at_store_time', 'cancelled_at',
    'actual_pickup_time_galaxy_a', 'actual_delivery_time_galaxy_a',
    'dasher_assigned_time_galaxy_a', 'dasher_at_store_time_galaxy_a'
]
for col in timestamp_columns:
    df[col] = pd.to_datetime(df[col])

# Convert active_date to datetime
df['active_date'] = pd.to_datetime(df['active_date'])

try:
    # Create table and load data
    df.to_sql('delivery_data', engine, if_exists='replace', index=False)
    print("Data successfully loaded to database!")
    
    # Test the connection with a simple query
    with engine.connect() as conn:
        result = conn.execute("SELECT COUNT(*) FROM delivery_data")
        count = result.fetchone()[0]
        print(f"Total records in database: {count}")

except Exception as e:
    print(f"An error occurred: {str(e)}") 