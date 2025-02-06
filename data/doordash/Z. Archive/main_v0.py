# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
import pandas as pd
import numpy as np
# Load and prepare the data
file_path = '~/code/data/doordash/Drive_Case_Study_Data_2024.csv'
data = pd.read_csv(file_path)
# %%
# Use the correct column names to filter the DataFrame based on key columns
data.info()

# Playing with the data
df_on_side = data.filter(items=['DASHER', 'MARKET_NUMBER', 'COMPOSITE_SCORE', 'COMPOSITE_STAR_RATING', 'NUM_FIVE_STARS', 'NUM_DELIVERIES', 'NUM_ON_TIME_DELIVERIES'], axis=1)

print(df_on_side.columns)

print(df_on_side.head())
# %%

# Question 1)

# Data pre-processing. We will drop the empty CANCELLED_AT column, convert time-related columns to datetime format, fill missing values for numerical columns with median, fill missing categorical values with 'Unknown', and create a new feature for actual delivery duration in minutes.

# Drop completely empty column
df_cleaned = data.drop(columns=["CANCELLED_AT"])

# Convert time-related columns to datetime format
time_columns = [
    "CREATED_AT", "QUOTED_DELIVERY_TIME", "ESTIMATED_DELIVERY_TIME",
    "ACTUAL_PICKUP_TIME", "ACTUAL_DELIVERY_TIME", "DASHER_ASSIGNED_TIME",
    "DASHER_CONFIRMED_TIME", "DASHER_AT_STORE_TIME", 
    "ACTUAL_PICKUP_TIME_GALAXY_A", "ACTUAL_DELIVERY_TIME_GALAXY_A",
    "DASHER_ASSIGNED_TIME_GALAXY_A", "DASHER_AT_STORE_TIME_GALAXY_A"
]

for col in time_columns:
    df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')

# CONSIDER IF THIS IS IDEAL APPROACH (LIKELY YES) 
# Fill missing values for numerical columns with median (robust to outliers)
num_cols = df_cleaned.select_dtypes(include=['float64']).columns
df_cleaned[num_cols] = df_cleaned[num_cols].fillna(df_cleaned[num_cols].median())

# Fill missing categorical values with 'Unknown'
cat_cols = df_cleaned.select_dtypes(include=['object']).columns
df_cleaned[cat_cols] = df_cleaned[cat_cols].fillna('Unknown')

# Create new feature: Actual delivery duration in minutes
df_cleaned["ACTUAL_DELIVERY_DURATION"] = (df_cleaned["ACTUAL_DELIVERY_TIME"] - df_cleaned["ACTUAL_PICKUP_TIME"]).dt.total_seconds() / 60

# Display cleaned data info and first few rows
df_cleaned.info(), df_cleaned.head()
# %%
""" 
Dasher Selection Process for Widget Deliveries

Since widget deliveries require higher precision and reliability, we should select Dashers based on key performance indicators. Given the differences between Dashattan (dense urban) and Doorlanta (sprawling suburban), we will adjust criteria accordingly.
1. Selection Criteria for Dashers

    General Requirements (Both Cities)
        Minimum composite star rating of 4.5+ (higher-rated Dashers are more reliable).
        Minimum of 500+ lifetime deliveries (ensures experience).
        Above-median on-time delivery percentage.

    MARKET_NAME-Specific Adjustments
        Dashattan (Urban)
            Prioritize bikers and motorbikes over cars for faster navigation in traffic.
            Focus on Dashers with high short-distance delivery efficiency.
        Doorlanta (Suburban)
            Prioritize Dashers with cars due to longer distances.
            Consider experience in handling long-distance deliveries efficiently. """

# %%

# Reassign data to df
df = df_cleaned

# Convert timestamps to datetime
time_cols = ["CREATED_AT", "ACTUAL_PICKUP_TIME", "ACTUAL_DELIVERY_TIME"]
for col in time_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Compute actual delivery duration in minutes
df["ACTUAL_DELIVERY_DURATION"] = (df["ACTUAL_DELIVERY_TIME"] - df["ACTUAL_PICKUP_TIME"]).dt.total_seconds() / 60

# Compute proportion of deliveries which are on time
df["ON_TIME_DELIVERY_RATE"] = df["NUM_ON_TIME_DELIVERIES"] / df["NUM_DELIVERIES"]

# Fill missing values
df.fillna({
    "COMPOSITE_STAR_RATING": df["COMPOSITE_STAR_RATING"].median(),  # Use median for numerical
    "NUM_DELIVERIES": df["NUM_DELIVERIES"].median(),
    "DASHER_VEHICLE_TYPE": "Unknown",  # Use 'Unknown' for categorical
}, inplace=True)
# %%
# First, how many drivers do we need? 
# Assuming the other drivers do not mind potentially higher demand, we could denote some drivers as responsible for only widgets. We are also assuming that all of these drivers will want to do the more careful, tedious, laborious widget deliveries. Finally, we're assuming that all the bikers have containers that can protect widgets (as widgets are more fragile than food).
# If widget demand is 35% of total food delivery demand, that means we need 35% of the Dashers that we normally have.
# Let's calculate the number of Dashers we need for widget deliveries in each city.


# Total number of Dashers per city for regular deliveries

dashattan_dashers = df[df["MARKET_NAME"] == "Dashattan"]
doorlanta_dashers = df[df["MARKET_NAME"] == "Doorlanta"]

dashattan_count = dashattan_dashers["DASHER"].nunique()
doorlanta_count = doorlanta_dashers["DASHER"].nunique()

dashattan_count, doorlanta_count

# Interesting - it seems there are only 22 Dashers in Dashattan and 27 Dashers in Doorlanta that meet the criteria.

# So for widget deliveries, we would need how many Dashers in each city?

dashattan_need = int(0.35 * dashattan_count)
doorlanta_need = int(0.35 * doorlanta_count)

dashattan_need, doorlanta_need
 
# It seems we need 8 Dashers in Dashattan and 10 Dashers in Doorlanta for widget deliveries. Let's see how many high-performing Dashers we have in each city.

# %%


# Filtering high-performing Dashers based on defined criteria
high_performing_dashers = df[
    (df["COMPOSITE_STAR_RATING"] >= 4.5) &
    (df["NUM_DELIVERIES"] >= 500) &
    (df["ON_TIME_DELIVERY_RATE"] > df["ON_TIME_DELIVERY_RATE"].median())
    ]

# Splitting by city (MARKET_NAME)
dashattan_dashers = high_performing_dashers[high_performing_dashers["MARKET_NAME"] == "Dashattan"]
doorlanta_dashers = high_performing_dashers[high_performing_dashers["MARKET_NAME"] == "Doorlanta"]

# Count selected Dashers per city (MARKET_NAME)
dashattan_count = dashattan_dashers["DASHER"].nunique()
doorlanta_count = doorlanta_dashers["DASHER"].nunique()

dashattan_count, doorlanta_count

# The number of selected Dashers for Dashattan is 5, and for Doorlanta is 7. Let's loosen up the criteria to see if we can get more Dashers.
# %%
decently_performing_dashers = df[
    (df["COMPOSITE_STAR_RATING"] >= 4.5) &
    (df["NUM_DELIVERIES"] >= 500) &
    (df["ON_TIME_DELIVERY_RATE"] > 0.05)
    ]
# Splitting by city (MARKET_NAME)
dashattan_dashers = decently_performing_dashers[decently_performing_dashers["MARKET_NAME"] == "Dashattan"]
doorlanta_dashers = decently_performing_dashers[decently_performing_dashers["MARKET_NAME"] == "Doorlanta"]

# Count selected Dashers per city (MARKET_NAME)
dashattan_count = dashattan_dashers["DASHER"].nunique()
doorlanta_count = doorlanta_dashers["DASHER"].nunique()

dashattan_count, doorlanta_count

# The number of selected Dashers for Dashattan is 7, and for Doorlanta is 10. This is sufficient for widget deliveries in both cities.

# Should the criteria be the same for both cities? Considerations include bikes versus cars.
# %%
print(dashattan_dashers.drop_duplicates(subset=["DASHER"]))
print(dashattan_dashers.drop_duplicates(subset=["VEHICLE"]))
# All Dashattan dashers are using bicycles.
print(doorlanta_dashers.drop_duplicates(subset=["DASHER"]))
print(doorlanta_dashers.drop_duplicates(subset=["VEHICLE"]))
# All Dashlanta dashers are using cars.
# As all Dashattan Dashers are using bicycles, we can assume that they are more experienced in navigating through traffic and short distances. We are okay with all Dashattan Dashers being bikes.
# We are also okay with all Dashlanta Dashers being cars, as they are necessary for handling long distances.
# %%

# Question 2)

# 2. Distributing Widget Satchels to Dashers
""" 
In Dashattan: Implement centralized pickup locations strategically placed near high-demand zones to maximize efficiency. Dashers should collect satchels at the beginning of their shifts to ensure they are ready for widget deliveries.
In Doorlanta: Due to the city’s sprawling nature, distribute satchels directly to the homes of the select group of full-time Dashers specializing in widget deliveries. If mailing satchels is cost-prohibitive due to their value or size, consider leveraging regional distribution hubs to manage logistics more effectively.
"""

# 3. Measuring Program Success
""" 
    Delivery Quality
        On-time delivery rate (percentage of widget orders delivered within quoted time).
        Delivery accuracy (percentage of orders delivered correctly without damage).

    Dasher Performance
        Average delivery duration (time from pickup to drop-off).
        Dasher ratings on widget deliveries.

    DoorDash Success (Profitability & Efficiency)
        Profit margin per widget delivery (revenue - operational costs).
        Average cost per delivery (including satchel logistics, Dasher incentives).

    Merchant Success
        Merchant rating of delivery service (feedback on timeliness, condition).

    Customer Satisfaction
        Customer star ratings for widget deliveries.
        Customer complaints per 100 deliveries (damaged/missing widgets). """