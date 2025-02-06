import pandas as pd
import numpy as np

# Load and inspect the data
file_path = '~/code/data/doordash/Drive_Case_Study_Data_2024.csv'
data = pd.read_csv(file_path)
data.info()

# Data Cleaning and Feature Engineering
# Step 1: Drop columns that are completely empty
cleaned_data = data.drop(columns=["CANCELLED_AT"])

# Step 2: Convert time-related columns to datetime format
# These columns capture various timestamps during the delivery process.
time_columns = [
    "CREATED_AT", "QUOTED_DELIVERY_TIME", "ESTIMATED_DELIVERY_TIME",
    "ACTUAL_PICKUP_TIME", "ACTUAL_DELIVERY_TIME", "DASHER_ASSIGNED_TIME",
    "DASHER_CONFIRMED_TIME", "DASHER_AT_STORE_TIME",
    "ACTUAL_PICKUP_TIME_GALAXY_A", "ACTUAL_DELIVERY_TIME_GALAXY_A",
    "DASHER_ASSIGNED_TIME_GALAXY_A", "DASHER_AT_STORE_TIME_GALAXY_A"
]

for col in time_columns:
    cleaned_data[col] = pd.to_datetime(cleaned_data[col], errors='coerce')

# Step 3: Handle missing values
# Numerical columns: Fill missing values with the median (robust to outliers)
numerical_cols = cleaned_data.select_dtypes(include=['float64']).columns
cleaned_data[numerical_cols] = cleaned_data[numerical_cols].fillna(cleaned_data[numerical_cols].median())

# Categorical columns: Fill missing values with 'Unknown'
categorical_cols = cleaned_data.select_dtypes(include=['object']).columns
cleaned_data[categorical_cols] = cleaned_data[categorical_cols].fillna('Unknown')

# Step 4: Create new feature for delivery duration (in minutes)
cleaned_data["ACTUAL_DELIVERY_DURATION"] = (
    cleaned_data["ACTUAL_DELIVERY_TIME"] - cleaned_data["ACTUAL_PICKUP_TIME"]
).dt.total_seconds() / 60

# Display cleaned data info and preview
cleaned_data.info()
print(cleaned_data.head())

# Reassign cleaned data to a working DataFrame for analysis
df = cleaned_data

# Additional Feature Engineering
# Calculate on-time delivery rate for each Dasher
df["ON_TIME_DELIVERY_RATE"] = df["NUM_ON_TIME_DELIVERIES"] / df["NUM_DELIVERIES"]

# Fill additional missing values with appropriate defaults
df.fillna({
    "COMPOSITE_STAR_RATING": df["COMPOSITE_STAR_RATING"].median(),
    "NUM_DELIVERIES": df["NUM_DELIVERIES"].median(),
    "DASHER_VEHICLE_TYPE": "Unknown"
}, inplace=True)

# Calculate required Dashers for widget deliveries based on demand
# Assuming widget deliveries are 35% of total delivery demand
dashattan_dashers = df[df["MARKET_NAME"] == "Dashattan"]
doorlanta_dashers = df[df["MARKET_NAME"] == "Doorlanta"]

dashattan_count = dashattan_dashers["DASHER"].nunique()
doorlanta_count = doorlanta_dashers["DASHER"].nunique()

dashattan_need = int(0.35 * dashattan_count)
doorlanta_need = int(0.35 * doorlanta_count)

print(f"Dashattan requires {dashattan_need} Dashers for widget deliveries.")
print(f"Doorlanta requires {doorlanta_need} Dashers for widget deliveries.")

# High-Performing Dasher Filtering
# Criteria: Composite star rating >= 4.5, 500+ lifetime deliveries, above-median on-time rate
high_performing_dashers = df[
    (df["COMPOSITE_STAR_RATING"] >= 4.5) &
    (df["NUM_DELIVERIES"] >= 500) &
    (df["ON_TIME_DELIVERY_RATE"] > df["ON_TIME_DELIVERY_RATE"].median())
]

# Splitting high-performing Dashers by city
dashattan_high = high_performing_dashers[high_performing_dashers["MARKET_NAME"] == "Dashattan"]
doorlanta_high = high_performing_dashers[high_performing_dashers["MARKET_NAME"] == "Doorlanta"]

print(f"High-performing Dashers in Dashattan: {dashattan_high['DASHER'].nunique()}")
print(f"High-performing Dashers in Doorlanta: {doorlanta_high['DASHER'].nunique()}")

# Loosening criteria to include more Dashers
decent_dashers = df[
    (df["COMPOSITE_STAR_RATING"] >= 4.5) &
    (df["NUM_DELIVERIES"] >= 500) &
    (df["ON_TIME_DELIVERY_RATE"] > 0.05)
]

dashattan_decent = decent_dashers[decent_dashers["MARKET_NAME"] == "Dashattan"]
doorlanta_decent = decent_dashers[decent_dashers["MARKET_NAME"] == "Doorlanta"]

print(f"Decently performing Dashers in Dashattan: {dashattan_decent['DASHER'].nunique()}")
print(f"Decently performing Dashers in Doorlanta: {doorlanta_decent['DASHER'].nunique()}")

# Evaluate vehicle types for each city
print("Dashattan Dasher Vehicles:")
print(dashattan_decent["VEHICLE"].value_counts())

print("Doorlanta Dasher Vehicles:")
print(doorlanta_decent["VEHICLE"].value_counts())

# Observations:
# - Dashattan Dashers predominantly use bicycles, which suits short-distance deliveries.
# - Doorlanta Dashers predominantly use cars, suitable for longer distances.

# Widget Satchel Distribution Plan
# In Dashattan: Centralized pickup locations near high-demand zones.
# In Doorlanta: Direct home delivery or regional hubs for efficiency if mailing is costly.

# Program Success Metrics
# 1. Delivery Quality: On-time rates, delivery accuracy.
# 2. Dasher Performance: Delivery duration, ratings.
# 3. Operational Success: Profit margin, cost per delivery.
# 4. Merchant Success: Feedback ratings.
# 5. Customer Satisfaction: Star ratings, complaints per 100 deliveries.
