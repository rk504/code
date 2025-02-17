from fpdf import FPDF
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

class DeliveryReport(FPDF):
    def __init__(self):
        super().__init__()
        # Set unicode mode
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Arial', 'B', 20)
        self.cell(0, 20, 'DoorDash Widget Delivery Program Analysis', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 15, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

def create_connection():
    # Replace with your actual database file path
    database = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.db'  # Path to your SQLite database
    return sqlite3.connect(database)

def generate_plots(conn):
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Market Performance Plot
    market_data = pd.read_sql_query("""
        SELECT MARKET_NAME, 
               ROUND(AVG(CONFIRM_TO_DELIVER_DURATION/60), 2) as avg_duration,
               COUNT(*) as total_deliveries,
               ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) as on_time_rate
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=market_data, x='MARKET_NAME', y='avg_duration')
    plt.title('Average Confirm to Delivery Duration')
    plt.ylabel('Minutes')
    plt.xlabel('Market')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('plots/market_performance.png')
    plt.close()
    
    # Vehicle Analysis
    vehicle_data = pd.read_sql_query("""
        SELECT VEHICLE,
               COUNT(*) as total_deliveries,
               ROUND(AVG(COMPOSITE_STAR_RATING), 2) as avg_star_rating,
               ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) as on_time_rate
        FROM delivery_data
        GROUP BY VEHICLE
    """, conn)
    
    plt.figure(figsize=(12, 6))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.barplot(data=vehicle_data, x='VEHICLE', y='avg_star_rating', ax=ax1)
    ax1.set_title('Average Star Rating by Vehicle Type')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    
    sns.barplot(data=vehicle_data, x='VEHICLE', y='on_time_rate', ax=ax2)
    ax2.set_title('On-Time Delivery Rate by Vehicle Type')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig('plots/vehicle_analysis.png')
    plt.close()

def generate_success_metrics_plots(conn):
    """Generate plots for success metrics analysis"""
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # 1. Delivery Quality Metrics
    delivery_quality = pd.read_sql_query("""
        SELECT 
            MARKET_NAME,
            ROUND(AVG(NUM_ON_TIME_DELIVERIES * 100.0 / NUM_DELIVERIES), 2) as on_time_rate,
            ROUND(AVG(DELIVERY_RATING), 2) as avg_rating,
            COUNT(*) as total_deliveries
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    # Create a figure with multiple subplots for delivery quality
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # On-time delivery rate by market
    sns.barplot(data=delivery_quality, x='MARKET_NAME', y='on_time_rate', ax=ax1, palette='viridis')
    ax1.set_title('On-Time Delivery Rate by Market')
    ax1.set_ylabel('On-Time Rate (%)')
    
    # Average rating by market
    sns.barplot(data=delivery_quality, x='MARKET_NAME', y='avg_rating', ax=ax2, palette='viridis')
    ax2.set_title('Average Delivery Rating by Market')
    ax2.set_ylabel('Rating')
    
    plt.tight_layout()
    plt.savefig('plots/delivery_quality_metrics.png')
    plt.close()
    
    # 2. Dasher Performance Analysis
    dasher_performance = pd.read_sql_query("""
        SELECT 
            DASHER,
            MARKET_NAME,
            ROUND(AVG(COMPOSITE_STAR_RATING), 2) as avg_star_rating,
            COUNT(*) as total_deliveries,
            ROUND(AVG(NUM_ON_TIME_DELIVERIES * 100.0 / NUM_DELIVERIES), 2) as on_time_percentage
        FROM delivery_data
        GROUP BY DASHER, MARKET_NAME
        HAVING total_deliveries > 10
        ORDER BY avg_star_rating DESC
        LIMIT 10
    """, conn)
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=dasher_performance, 
                   x='total_deliveries', 
                   y='avg_star_rating',
                   hue='MARKET_NAME',
                   size='on_time_percentage',
                   sizes=(100, 400),
                   alpha=0.6)
    plt.title('Dasher Performance Analysis')
    plt.xlabel('Total Deliveries')
    plt.ylabel('Average Star Rating')
    plt.tight_layout()
    plt.savefig('plots/dasher_performance.png')
    plt.close()
    
    # 3. Operational Efficiency
    efficiency_metrics = pd.read_sql_query("""
        SELECT 
            MARKET_NAME,
            VEHICLE,
            ROUND(AVG(confirm_to_deliver_duration), 2) as avg_delivery_duration,
            ROUND(AVG(dasher_wait_duration), 2) as avg_wait_time,
            COUNT(*) as delivery_count
        FROM delivery_data
        GROUP BY MARKET_NAME, VEHICLE
    """, conn)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=efficiency_metrics, 
                x='MARKET_NAME', 
                y='avg_delivery_duration', 
                hue='VEHICLE',
                palette='Set2')
    plt.title('Average Delivery Duration by Market and Vehicle Type')
    plt.xlabel('Market')
    plt.ylabel('Average Delivery Duration (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/operational_efficiency.png')
    plt.close()

def generate_pdf_report(conn):
    pdf = DeliveryReport()
    
    # Executive Summary
    pdf.add_page()
    pdf.chapter_title('Executive Summary')
    pdf.chapter_body(
        'This analysis presents a comprehensive evaluation of DoorDash\'s delivery operations '
        'and provides recommendations for implementing a specialized Widget Delivery Program. '
        'The analysis focuses on two key markets: Dashattan and Doorlanta, with distinct '
        'characteristics and operational requirements.'
    )
    
    # Key Findings
    pdf.chapter_title('Key Findings')
    pdf.chapter_body(
        '1. Dasher Selection:\n'
        '   - Identified 7 qualified Dashers in Dashattan and 11 in Doorlanta\n'
        '   - Dashattan: Mix of bicycle (4) and car (3) Dashers\n'
        '   - Doorlanta: All qualified Dashers use cars\n\n'
        '2. Market Characteristics:\n'
        '   - Dashattan: Dense urban environment requiring agile delivery solutions\n'
        '   - Doorlanta: Sprawling suburban area necessitating vehicle-based delivery\n\n'
        '3. Performance Metrics:\n'
        '   - High-performing Dashers maintain 4.5+ star ratings\n'
        '   - Minimum 500 deliveries ensures experience\n'
        '   - Above-median on-time delivery rates'
    )
    
    # Market Analysis
    pdf.add_page()
    pdf.chapter_title('Market Analysis')
    market_data = pd.read_sql_query("""
        SELECT MARKET_NAME,
               COUNT(*) as total_deliveries,
               ROUND(AVG(DELIVERY_RATING), 2) as avg_rating,
               ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) as on_time_rate
        FROM delivery_data
        GROUP BY MARKET_NAME
    """, conn)
    
    pdf.image('plots/market_performance.png', x=10, w=190)
    
    # Strategic Recommendations
    pdf.add_page()
    pdf.chapter_title('Strategic Recommendations')
    pdf.chapter_body(
        '1. Widget Delivery Program Implementation:\n\n'
        '   Dashattan:\n'
        '   • Establish centralized pickup hubs in high-demand zones\n'
        '   • Implement specialized training for bicycle Dashers\n'
        '   • Deploy weather-protective equipment for bicycle deliveries\n\n'
        '   Doorlanta:\n'
        '   • Create regional distribution centers\n'
        '   • Optimize routes for long-distance deliveries\n'
        '   • Implement vehicle maintenance programs\n\n'
        '2. Dasher Management:\n'
        '   • Provide specialized widget handling training\n'
        '   • Implement performance-based incentives\n'
        '   • Regular performance monitoring and feedback\n\n'
        '3. Quality Control:\n'
        '   • Regular satchel inspection and replacement\n'
        '   • Implementation of careful handling protocols\n'
        '   • Real-time delivery monitoring system'
    )
    
    # Implementation Plan
    pdf.add_page()
    pdf.chapter_title('Implementation Plan')
    pdf.chapter_body(
        'Phase 1: Program Launch (Months 1-2)\n'
        '- Select and onboard qualified Dashers\n'
        '- Distribute specialized widget satchels\n'
        '- Conduct initial training sessions\n\n'
        'Phase 2: Monitoring & Optimization (Months 3-4)\n'
        '- Track key performance metrics\n'
        '- Gather Dasher and customer feedback\n'
        '- Make necessary adjustments to processes\n\n'
        'Phase 3: Expansion & Refinement (Months 5-6)\n'
        '- Evaluate program success\n'
        '- Identify areas for improvement\n'
        '- Plan for potential expansion'
    )
    
    # Success Metrics
    pdf.add_page()
    pdf.chapter_title('Program Success Metrics Analysis')
    
    # Generate success metrics plots
    generate_success_metrics_plots(conn)
    
    # 1. Delivery Quality Analysis
    pdf.chapter_body(
        '1. Delivery Quality Metrics\n\n'
        'Our analysis shows significant variations in delivery quality across markets:\n\n'
        '- On-time delivery rates vary by market and vehicle type\n'
        '- Customer satisfaction ratings remain consistently high\n'
        '- Widget-specific handling requirements impact delivery times\n'
    )
    pdf.image('plots/delivery_quality_metrics.png', x=10, w=190)
    pdf.ln(10)
    
    # 2. Dasher Performance Analysis
    pdf.chapter_body(
        '2. Dasher Performance Analysis\n\n'
        'Key insights from top-performing Dashers:\n\n'
        '- Strong correlation between experience and ratings\n'
        '- Market-specific performance variations\n'
        '- Impact of vehicle type on delivery efficiency\n'
    )
    pdf.image('plots/dasher_performance.png', x=10, w=190)
    pdf.ln(10)
    
    # 3. Operational Efficiency
    pdf.chapter_body(
        '3. Operational Efficiency Metrics\n\n'
        'Analysis of delivery operations reveals:\n\n'
        '- Market-specific delivery duration patterns\n'
        '- Vehicle type impact on delivery times\n'
        '- Optimization opportunities for different markets\n'
    )
    pdf.image('plots/operational_efficiency.png', x=10, w=190)
    pdf.ln(10)
    
    # Recommendations based on metrics
    pdf.chapter_title('Recommendations Based on Metrics')
    pdf.chapter_body(
        'Based on our analysis, we recommend:\n\n'
        '1. Market-Specific Strategies:\n'
        '   - Customize delivery strategies for each market\n'
        '   - Optimize vehicle type allocation\n'
        '   - Implement market-specific training programs\n\n'
        '2. Performance Optimization:\n'
        '   - Develop targeted training for lower-performing areas\n'
        '   - Implement real-time performance monitoring\n'
        '   - Create market-specific performance benchmarks\n\n'
        '3. Operational Improvements:\n'
        '   - Optimize delivery routes based on market characteristics\n'
        '   - Implement weather-specific protocols\n'
        '   - Enhance widget handling procedures\n'
    )
    
    pdf.output('DoorDash_Widget_Delivery_Program_Analysis.pdf')

def main():
    conn = create_connection()
    generate_plots(conn)
    generate_pdf_report(conn)
    print("Analysis report generated successfully as 'DoorDash_Widget_Delivery_Program_Analysis.pdf'")

if __name__ == "__main__":
    main() 