-- Create table for delivery data
CREATE TABLE delivery_data (
    delivery_name VARCHAR(50),
    delivery_rating INTEGER,
    market_number INTEGER,
    market_name VARCHAR(50),
    timezone VARCHAR(50),
    dasher VARCHAR(50),
    is_first_delivery BOOLEAN,
    vehicle VARCHAR(20),
    created_at TIMESTAMP,
    quoted_delivery_time TIMESTAMP,
    estimated_delivery_time TIMESTAMP,
    asap BOOLEAN,
    fraudulent BOOLEAN,
    actual_pickup_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    dasher_assigned_time TIMESTAMP,
    manually_assigned BOOLEAN,
    dasher_confirmed_time TIMESTAMP,
    dasher_at_store_time TIMESTAMP,
    cancelled_at TIMESTAMP,
    active_date DATE,
    composite_score DECIMAL(10,2),
    subtotal INTEGER,
    confirm_to_deliver_duration INTEGER,
    dasher_to_restaurant_duration INTEGER,
    dasher_wait_duration INTEGER,
    restaurant_to_customer_duration INTEGER,
    was_batched BOOLEAN,
    total_item_count INTEGER,
    dasher_to_store_time_category VARCHAR(20),
    actual_pickup_time_galaxy_a TIMESTAMP,
    actual_delivery_time_galaxy_a TIMESTAMP,
    dasher_assigned_time_galaxy_a TIMESTAMP,
    dasher_at_store_time_galaxy_a TIMESTAMP,
    composite_star_rating DECIMAL(10,2),
    num_five_stars INTEGER,
    num_deliveries INTEGER,
    num_on_time_deliveries INTEGER
);

-- Create indexes for common query columns
CREATE INDEX idx_market_name ON delivery_data(market_name);
CREATE INDEX idx_dasher ON delivery_data(dasher);
CREATE INDEX idx_active_date ON delivery_data(active_date);
CREATE INDEX idx_vehicle ON delivery_data(vehicle);

-- Sample analytical queries

-- Average delivery rating by market
SELECT 
    market_name,
    ROUND(AVG(delivery_rating), 2) as avg_rating,
    COUNT(*) as total_deliveries
FROM delivery_data
GROUP BY market_name;

-- Performance metrics by vehicle type
SELECT 
    vehicle,
    COUNT(*) as total_deliveries,
    ROUND(AVG(confirm_to_deliver_duration), 2) as avg_delivery_duration,
    ROUND(AVG(composite_star_rating), 2) as avg_star_rating
FROM delivery_data
GROUP BY vehicle;

-- Top performing dashers
SELECT 
    dasher,
    COUNT(*) as total_deliveries,
    ROUND(AVG(delivery_rating), 2) as avg_rating,
    ROUND(AVG(composite_star_rating), 2) as avg_star_rating,
    SUM(num_five_stars) as total_five_stars
FROM delivery_data
GROUP BY dasher
HAVING COUNT(*) > 10
ORDER BY avg_rating DESC
LIMIT 10;

-- Fraudulent order analysis
SELECT 
    market_name,
    COUNT(*) as total_orders,
    SUM(CASE WHEN fraudulent THEN 1 ELSE 0 END) as fraudulent_orders,
    ROUND(100.0 * SUM(CASE WHEN fraudulent THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_percentage
FROM delivery_data
GROUP BY market_name;

-- Delivery timing analysis
SELECT 
    market_name,
    ROUND(AVG(dasher_to_restaurant_duration), 2) as avg_to_restaurant_time,
    ROUND(AVG(dasher_wait_duration), 2) as avg_wait_time,
    ROUND(AVG(restaurant_to_customer_duration), 2) as avg_to_customer_time
FROM delivery_data
WHERE dasher_to_restaurant_duration IS NOT NULL 
    AND dasher_wait_duration IS NOT NULL 
    AND restaurant_to_customer_duration IS NOT NULL
GROUP BY market_name;

-- Order value distribution
SELECT 
    CASE 
        WHEN subtotal < 1500 THEN 'Low (<$15)'
        WHEN subtotal < 3000 THEN 'Medium ($15-$30)'
        ELSE 'High (>$30)'
    END as order_value_category,
    COUNT(*) as order_count,
    ROUND(AVG(delivery_rating), 2) as avg_rating
FROM delivery_data
GROUP BY 
    CASE 
        WHEN subtotal < 1500 THEN 'Low (<$15)'
        WHEN subtotal < 3000 THEN 'Medium ($15-$30)'
        ELSE 'High (>$30)'
    END;

-- Time of day analysis
SELECT 
    EXTRACT(HOUR FROM created_at) as hour_of_day,
    COUNT(*) as order_count,
    ROUND(AVG(confirm_to_deliver_duration), 2) as avg_delivery_duration
FROM delivery_data
GROUP BY EXTRACT(HOUR FROM created_at)
ORDER BY hour_of_day;

-- On-time delivery performance
SELECT 
    dasher,
    COUNT(*) as total_deliveries,
    SUM(num_on_time_deliveries) as on_time_deliveries,
    ROUND(100.0 * SUM(num_on_time_deliveries) / COUNT(*), 2) as on_time_percentage
FROM delivery_data
WHERE num_on_time_deliveries IS NOT NULL
GROUP BY dasher
HAVING COUNT(*) > 10
ORDER BY on_time_percentage DESC
LIMIT 10; 