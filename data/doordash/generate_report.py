from fpdf import FPDF
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

class DeliveryReport(FPDF):
    def header(self):
        # Add logo if needed
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Delivery Data Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_connection():
    # Replace with your actual database file path
    database = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.db'  # Path to your SQLite database
    return sqlite3.connect(database)

def generate_plots(conn):
    # Create plots directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Query and create visualizations
    market_data = pd.read_sql_query("""
        SELECT MARKET_NAME, 
               ROUND(AVG(DELIVERY_RATING), 2) as avg_rating,
               COUNT(*) as total_deliveries
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    # Debugging output
    print("Market Data:")
    print(market_data.head())  # Check the first few rows of the DataFrame
    print("Columns in Market Data:", market_data.columns)  # Check the column names

    # Check if 'MARKET_NAME' is in the DataFrame
    if 'MARKET_NAME' not in market_data.columns:
        print("Error: 'MARKET_NAME' column not found in market_data.")
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(data=market_data, x='MARKET_NAME', y='avg_rating')
    plt.title('Average Delivery Rating by Market')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/market_performance.png')
    plt.close()
    
    # Vehicle Performance Plot
    vehicle_data = pd.read_sql_query("""
        SELECT VEHICLE,
               COUNT(*) as total_deliveries,
               ROUND(AVG(COMPOSITE_STAR_RATING), 2) as avg_star_rating
        FROM delivery_data
        GROUP BY VEHICLE
    """, conn)
    
    print("Vehicle Data:")
    print(vehicle_data.head())  # Check the first few rows of the DataFrame

    plt.figure(figsize=(10, 6))
    sns.barplot(data=vehicle_data, x='VEHICLE', y='avg_star_rating')
    plt.title('Average Star Rating by Vehicle Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/vehicle_performance.png')
    plt.close()

    # On-Time Delivery Rate Plot
    on_time_data = pd.read_sql_query("""
        SELECT MARKET_NAME,
               ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) as avg_on_time_rate
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    print("On-Time Delivery Data:")
    print(on_time_data.head())  # Check the first few rows of the DataFrame

    plt.figure(figsize=(10, 6))
    sns.barplot(data=on_time_data, x='MARKET_NAME', y='avg_on_time_rate')
    plt.title('Average On-Time Delivery Rate by Market')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/on_time_delivery_rate.png')
    plt.close()

def generate_pdf_report(conn):
    pdf = DeliveryReport()
    pdf.add_page()
    
    # Title and Introduction
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Delivery Data Analysis Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Market Analysis Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Market Analysis', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    market_data = pd.read_sql_query("""
        SELECT MARKET_NAME,
               ROUND(AVG(DELIVERY_RATING), 2) as avg_rating,
               COUNT(*) as total_deliveries
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    for _, row in market_data.iterrows():
        pdf.cell(0, 10, 
                f"{row['MARKET_NAME']}: {row['total_deliveries']} deliveries, "
                f"Avg Rating: {row['avg_rating']}", 0, 1)
    
    # Add market performance plot
    pdf.image('plots/market_performance.png', x=10, w=190)
    pdf.ln(10)
    
    # Vehicle Analysis Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Vehicle Performance Analysis', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    vehicle_data = pd.read_sql_query("""
        SELECT VEHICLE,
               COUNT(*) as total_deliveries,
               ROUND(AVG(COMPOSITE_STAR_RATING), 2) as avg_star_rating
        FROM delivery_data
        GROUP BY VEHICLE
    """, conn)
    
    for _, row in vehicle_data.iterrows():
        pdf.cell(0, 10, 
                f"{row['VEHICLE']}: {row['total_deliveries']} deliveries, "
                f"Avg Rating: {row['avg_star_rating']}", 0, 1)
    
    # Add vehicle performance plot
    pdf.image('plots/vehicle_performance.png', x=10, w=190)
    pdf.ln(10)

    # On-Time Delivery Rate Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'On-Time Delivery Rate Analysis', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    on_time_data = pd.read_sql_query("""
        SELECT MARKET_NAME,
               ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) as avg_on_time_rate
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    for _, row in on_time_data.iterrows():
        pdf.cell(0, 10, 
                f"{row['MARKET_NAME']}: Avg On-Time Delivery Rate: {row['avg_on_time_rate']}", 0, 1)
    
    # Add on-time delivery rate plot
    pdf.image('plots/on_time_delivery_rate.png', x=10, w=190)
    pdf.ln(10)

    # Recommendations Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Recommendations', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 
        "1. Focus on improving the on-time delivery rate in markets with lower performance.\n"
        "2. Consider incentivizing Dashers with higher ratings to take on more deliveries.\n"
        "3. Evaluate the vehicle types used by Dashers and provide training for efficient delivery methods.\n"
        "4. Implement a feedback loop with Dashers to understand challenges faced during deliveries.\n"
        "5. Monitor the performance of Dashers regularly and adjust criteria for selection based on market needs."
    )

    # Save the PDF
    pdf.output('delivery_analysis_report.pdf')

def main():
    # Create database connection
    conn = create_connection()
    
    # Generate plots
    generate_plots(conn)
    
    # Generate PDF report
    generate_pdf_report(conn)
    
    print("Report generated successfully as 'delivery_analysis_report.pdf'")

if __name__ == "__main__":
    main() 