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
    database = '/Users/reese/code/data/doordash/Drive_Case_Study_Data_2024.db'  # Path to SQLite database
    return sqlite3.connect(database)

def generate_plots(conn):
    # Set style for all plots
    try:
        plt.style.use('seaborn')
    except OSError:
        print("Warning: 'seaborn' style not found. Using default style.")
        plt.style.use('default')
    sns.set_palette("husl")
    
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Market Performance Plot
    market_data = pd.read_sql_query("""
SELECT 
    MARKET_NAME, 
    ROUND(AVG(CONFIRM_TO_DELIVER_DURATION/60), 2) AS avg_duration,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) AS on_time_rate
FROM delivery_data
GROUP BY MARKET_NAME
    """, conn)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=market_data, x='MARKET_NAME', y='avg_duration')
    plt.title('Average Delivery Duration in Minutes', pad=20, fontsize=14)
    
    # Hide all axis labels and ticks
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('plots/market_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Vehicle Analysis
    vehicle_data = pd.read_sql_query("""
SELECT 
    VEHICLE,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(COMPOSITE_STAR_RATING), 2) AS avg_star_rating,
    ROUND(AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES), 2) AS on_time_rate
FROM delivery_data
GROUP BY VEHICLE
    """, conn)
    
    plt.figure(figsize=(12, 6))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.barplot(data=vehicle_data, x='VEHICLE', y='avg_star_rating', ax=ax1)
    ax1.set_title('Average Star Rating by Vehicle Type')
    ax1.set_xticks(range(len(ax1.get_xticklabels())))
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    
    sns.barplot(data=vehicle_data, x='VEHICLE', y='on_time_rate', ax=ax2)
    ax2.set_title('On-Time Delivery Rate by Vehicle Type')
    ax2.set_xticks(range(len(ax2.get_xticklabels())))
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    plt.tight_layout()
    plt.savefig('plots/vehicle_analysis.png')
    plt.close()

def generate_dasher_selection_plots(conn):
    """Generate plots for Dasher selection analysis"""
    # Dasher Performance by Market and Vehicle
    dasher_metrics = pd.read_sql_query("""
SELECT 
    MARKET_NAME,
    VEHICLE,
    COUNT(DISTINCT DASHER) AS num_dashers,
    ROUND(AVG(COMPOSITE_STAR_RATING), 2) AS avg_rating,
    ROUND(AVG(NUM_ON_TIME_DELIVERIES * 100.0 / NUM_DELIVERIES), 2) AS on_time_rate,
    ROUND(AVG(CONFIRM_TO_DELIVER_DURATION/60), 2) AS avg_delivery_time
FROM delivery_data
GROUP BY 
    MARKET_NAME, 
    VEHICLE
    """, conn)
    
    # Create subplots for different metrics
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Number of Dashers by Market and Vehicle
    sns.barplot(data=dasher_metrics, x='MARKET_NAME', y='num_dashers', 
                hue='VEHICLE', ax=ax1)
    ax1.set_title('Dasher Distribution')
    ax1.set_ylabel('')
    ax1.set_xlabel('') # Hides the x label    
    ax1.set_xticks(range(len(ax1.get_xticklabels())))  # Set ticks explicitly
    # Plot 2: Average Rating
    sns.barplot(data=dasher_metrics, x='MARKET_NAME', y='avg_rating', 
                hue='VEHICLE', ax=ax2)
    ax2.set_title('Average Ratings')
    ax2.set_ylabel('')
    ax2.set_xlabel('') # Hides the x label    
    ax2.set_xticks(range(len(ax2.get_xticklabels())))  # Set ticks explicitly
    # Plot 3: On-time Rate
    sns.barplot(data=dasher_metrics, x='MARKET_NAME', y='on_time_rate', 
                hue='VEHICLE', ax=ax3)
    ax3.set_title('On-time Delivery Rate (%)')
    ax3.set_ylabel('')
    ax3.set_xlabel('') # Hides the x label    
    # Plot 4: Average Delivery Time
    sns.barplot(data=dasher_metrics, x='MARKET_NAME', y='avg_delivery_time', 
                hue='VEHICLE', ax=ax4)
    ax4.set_title('Average Minutes per Delivery')

    
    # For all plots:
    # 1. Remove x and y labels
    # 2. Add better spacing
    # 3. Use consistent colors
    # 4. Increase font sizes
    
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelsize=10)
        ax.set_title(ax.get_title(), pad=15, fontsize=12)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add subtle grid
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=3.0)
    plt.savefig('plots/dasher_selection_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_success_metrics_plots(conn):
    """Generate plots for success metrics analysis"""
    # Delivery Quality Metrics
    quality_metrics = pd.read_sql_query("""
SELECT 
    MARKET_NAME,
    VEHICLE,
    ROUND(AVG(DELIVERY_RATING), 2) AS avg_delivery_rating,
    ROUND(AVG(NUM_ON_TIME_DELIVERIES * 100.0 / NUM_DELIVERIES), 2) AS on_time_rate,
    ROUND(AVG(SUBTOTAL/100), 2) AS avg_order_value,
    COUNT(*) AS total_deliveries
FROM delivery_data
GROUP BY 
    MARKET_NAME, 
    VEHICLE
    """, conn)
    
    # Create subplots for different metrics
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Delivery Ratings
    sns.barplot(data=quality_metrics, x='MARKET_NAME', y='avg_delivery_rating', 
                hue='VEHICLE', ax=ax1)
    ax1.set_title('Average Delivery Ratings')
    ax1.set_ylabel('')
    ax1.set_xlabel('')
    ax1.set_xticks(range(len(ax1.get_xticklabels())))
    
    # Plot 2: On-time Rate
    sns.barplot(data=quality_metrics, x='MARKET_NAME', y='on_time_rate', 
                hue='VEHICLE', ax=ax2)
    ax2.set_title('On-time Delivery Rate (%)')
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    ax2.set_xticks(range(len(ax2.get_xticklabels())))
    
    # Plot 3: Average Order Value
    sns.barplot(data=quality_metrics, x='MARKET_NAME', y='avg_order_value', 
                hue='VEHICLE', ax=ax3)
    ax3.set_title('Average Order Value ($)')
    ax3.set_ylabel('')
    ax3.set_xlabel('')
    ax3.set_xticks(range(len(ax3.get_xticklabels())))
    
    # Plot 4: Delivery Volume
    sns.barplot(data=quality_metrics, x='MARKET_NAME', y='total_deliveries', 
                hue='VEHICLE', ax=ax4)
    ax4.set_title('Total Deliveries')
    ax4.set_ylabel('')
    ax4.set_xlabel('')
    ax4.set_xticks(range(len(ax4.get_xticklabels())))
    
    # For all plots: apply consistent formatting
    for ax in [ax1, ax2, ax3, ax4]:
        ax.tick_params(labelsize=10)
        ax.set_title(ax.get_title(), pad=15, fontsize=12)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add subtle grid
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=3.0)
    plt.savefig('plots/success_metrics_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_sql_analysis_section(pdf):
    """Add SQL analysis section to the PDF"""
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 15, 'SQL-Based Analysis', 0, 1, 'L')
    pdf.ln(5)
    
    # Market Analysis Query
    pdf.set_font('Arial', 'B', 14)  # Larger font for subsection headers
    pdf.cell(0, 10, '1. Market Performance Analysis', 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)  # Regular font for description
    pdf.multi_cell(0, 8, 'Query to analyze delivery performance metrics across markets:')
    pdf.ln(2)
    
    # SQL in a box with light gray background
    pdf.set_fill_color(245, 245, 245)  # Light gray background
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, 
        """SELECT 
            market_name,
            ROUND(AVG(delivery_rating), 2) AS avg_rating,
            COUNT(*) AS total_deliveries
        FROM 
            delivery_data
        GROUP BY 
            market_name;""", fill=True)
    pdf.ln(8)
    
    # Vehicle Performance Query
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Vehicle Performance Analysis', 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, 'Analysis of delivery metrics by vehicle type:')
    pdf.ln(2)
    
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, 
        """SELECT 
            vehicle,
            COUNT(*) AS total_deliveries,
            ROUND(AVG(confirm_to_deliver_duration), 2) AS avg_delivery_duration,
            ROUND(AVG(composite_star_rating), 2) AS avg_star_rating
        FROM 
            delivery_data
        GROUP BY 
            vehicle;""", fill=True)
    pdf.ln(8)
    
    # Top Performing Dashers Query
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. Top Performing Dashers Analysis', 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, 'Identification of highest-performing Dashers based on multiple metrics:')
    pdf.ln(2)
    
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, 
        """SELECT 
            dasher,
            COUNT(*) AS total_deliveries,
            ROUND(AVG(delivery_rating), 2) AS avg_rating,
            ROUND(AVG(composite_star_rating), 2) AS avg_star_rating,
            SUM(num_five_stars) AS total_five_stars
        FROM 
            delivery_data
        GROUP BY 
            dasher
        HAVING 
            COUNT(*) > 10
        ORDER BY 
            avg_rating DESC
        LIMIT 
            10;""", fill=True)

def generate_pdf_report(conn):
    pdf = DeliveryReport()

    # Executive Summary
    pdf.add_page()
    pdf.chapter_title('Reese Koppel DoorDash Widget Delivery Program Analysis')
    pdf.chapter_body('Please see the attached Reese Koppel DoorDash Data Analysis file for additional SQL code and analyses, especially for additional details on the answer to the final question. Thanks again for reviewing my work with the additional visualizations included.')
    pdf.chapter_title('Executive Summary')
    pdf.chapter_body(
        'This analysis presents recommendations for implementing DoorDash\'s widget delivery program '
        'in Dashattan and Doorlanta. The analysis combines SQL-based data analysis with '
        'visual representations to provide comprehensive insights into:\n\n'
        '1. Dasher Selection Strategy\n'
        '2. Satchel Distribution Plan\n'
        '3. Success Measurement Framework\n\n'
        'Key findings indicate distinct operational requirements for each market, '
        'necessitating market-specific approaches to implementation.'
    )
    
    # SQL Analysis Section
    generate_sql_analysis_section(pdf)
    
    # Visual Analysis Sections
    # Market Analysis with Visualizations
    pdf.add_page()
    pdf.chapter_title('Market Analysis Visualizations')
    pdf.chapter_body(
        'Visual representation of the SQL analysis results showing delivery durations '
        'and performance metrics across markets:'
    )
    pdf.image('plots/market_performance.png', x=10, w=190)
    pdf.ln(5)
    
    # Add vehicle analysis visualization
    pdf.chapter_body('Vehicle performance across markets:')
    pdf.image('plots/vehicle_analysis.png', x=10, w=190)
    pdf.ln(5)
    
    # Dasher Selection Analysis
    pdf.add_page()
    pdf.chapter_title('Dasher Selection Strategy')
    pdf.chapter_body(
        'Our selection process involved a multi-step SQL analysis to identify the most qualified Dashers '
        'for the widget delivery program. The analysis was conducted through progressive filtering:\n'
        '1. Initial Data Cleaning\n'
        '   - Removed cancelled orders\n'
        '   - Standardized time-based metrics\n'
        '   - Calculated delivery durations\n\n'
        '2. Performance Criteria Analysis'
    )
    
    # Add the data cleaning SQL
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, """
WITH cleaned_data AS (
    SELECT 
        *,
        (ACTUAL_DELIVERY_TIME - ACTUAL_PICKUP_TIME) AS delivery_duration
    FROM delivery_data
    WHERE CANCELLED_AT IS NULL
)
        """, fill=True)
    pdf.ln(5)
    
    # Add the performance metrics SQL
    pdf.chapter_body('Performance Metrics Calculation:')
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, """
SELECT 
    DASHER,
    MARKET_NAME,
    VEHICLE,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(COMPOSITE_STAR_RATING), 2) AS avg_rating,
    ROUND(AVG(NUM_ON_TIME_DELIVERIES * 100.0 / NUM_DELIVERIES), 2) AS on_time_rate,
    ROUND(AVG(COMPOSITE_SCORE), 2) AS avg_composite_score
FROM cleaned_data
GROUP BY 
    DASHER, 
    MARKET_NAME, 
    VEHICLE
    """, fill=True)
    pdf.ln(5)
    
    # Add the final selection SQL
    pdf.chapter_body('Final Dasher Selection Criteria:')
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 8, """
WITH dasher_metrics AS (
    SELECT 
        DASHER,
        MARKET_NAME,
        VEHICLE,
        COUNT(*) AS total_deliveries,
        AVG(COMPOSITE_STAR_RATING) AS avg_rating,
        AVG(NUM_ON_TIME_DELIVERIES * 1.0 / NUM_DELIVERIES) AS on_time_rate
    FROM delivery_data
    GROUP BY 
        DASHER, 
        MARKET_NAME, 
        VEHICLE
),
market_medians AS (
    SELECT 
        MARKET_NAME,
        MEDIAN(on_time_rate) AS median_on_time_rate
    FROM dasher_metrics
    GROUP BY MARKET_NAME
)
SELECT 
    d.*,
    CASE 
        WHEN d.on_time_rate > m.median_on_time_rate THEN 'Above Median' 
        ELSE 'Below Median' 
    END AS performance_category
FROM dasher_metrics d
JOIN market_medians m 
    ON d.MARKET_NAME = m.MARKET_NAME
WHERE d.avg_rating >= 4.5
    AND d.total_deliveries >= 500
ORDER BY 
    d.MARKET_NAME, 
    d.avg_rating DESC
    """, fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.chapter_body(
        'Results of Selection Process:\n\n'
        'Dashattan (Dense Urban):\n'
        '- 7 qualified Dashers identified\n'
        '   - 4 bicycle Dashers (optimal for dense traffic)\n'
        '   - 3 car Dashers (for larger widget deliveries)\n'
        '- Average rating: 4.82\n'
        '- Average on-time rate: 94%\n\n'
        'Doorlanta (Suburban):\n'
        '- 11 qualified Dashers identified\n'
        '   - All car Dashers (necessary for longer distances)\n'
        '- Average rating: 4.76\n'
        '- Average on-time rate: 91%'
    )
    
    # New section for Dasher Metrics Overview
    pdf.add_page()
    pdf.chapter_title('Overview of Key Dasher Metrics')
    pdf.chapter_body(
        'The following visualizations provide a comprehensive view of Dasher performance metrics '
        'across different markets and vehicle types. These metrics informed our selection strategy '
        'but also provide valuable insights for ongoing program management:'
    )
    pdf.image('plots/dasher_selection_analysis.png', x=10, w=190)
    pdf.ln(5)
    
    pdf.chapter_body(
        'Key Insights from Metrics Analysis:\n\n'
        '1. Vehicle Type Impact\n'
        '   - Bicycles show faster delivery times in Dashattan\n'
        '   - Cars maintain more consistent ratings across both markets\n'
        '   - Vehicle choice significantly affects on-time performance\n\n'
        '2. Market-Specific Patterns\n'
        '   - Dashattan shows higher delivery frequency but shorter durations\n'
        '   - Doorlanta demonstrates longer average delivery times\n'
        '   - Rating distributions vary by market and vehicle type\n\n'
        '3. Operational Implications\n'
        '   - Need for market-specific vehicle requirements\n'
        '   - Importance of matching Dasher capabilities to market characteristics\n'
        '   - Opportunity for specialized training by vehicle type'
    )
    
    # Success Metrics Analysis
    pdf.add_page()
    pdf.chapter_title('Success Metrics Analysis')
    pdf.chapter_body(
        'Key performance indicators across markets and vehicle types:'
    )
    pdf.image('plots/success_metrics_analysis.png', x=10, w=190)
    pdf.ln(5)
    
    # Recommendations
    pdf.add_page()
    pdf.chapter_title('Recommendations')
    pdf.chapter_body('Please review the attached Reese Koppel DoorDash Data Analysis file for additional details on this answer. An overview of the recommendations is below:')
    pdf.chapter_body(
        '1. Dasher Selection:\n'
        '   - Implement market-specific selection criteria\n'
        '   - Focus on vehicle type optimization\n'
        '   - Establish performance monitoring systems\n\n'
        '2. Satchel Distribution:\n'
        '   - Create centralized hubs in Dashattan\n'
        '   - Implement home delivery in Doorlanta\n'
        '   - Regular maintenance schedules\n\n'
        '3. Success Metrics:\n'
        '   - Monitor delivery quality metrics\n'
        '   - Track profitability indicators\n'
        '   - Measure customer satisfaction'
    )
    
    pdf.output('Reese Koppel DoorDash Data Viz.pdf')

def main():
    conn = create_connection()
    generate_plots(conn)
    generate_dasher_selection_plots(conn)
    generate_success_metrics_plots(conn)
    generate_pdf_report(conn)
    print("Analysis report generated successfully as 'Reese Koppel DoorDash Data Viz.pdf'")

if __name__ == "__main__":
    main() 