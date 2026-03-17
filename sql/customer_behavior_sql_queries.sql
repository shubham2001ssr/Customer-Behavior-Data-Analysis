-- ==========================================
-- Customer Behavior Data Analysis - SQL Queries
-- ==========================================
-- Dataset: customer_shopping_data
-- Note: Replace 'customer_shopping_data' with your actual table name if different in your RDBMS.

-- 1. Total Revenue & Basic Analytics by Category
SELECT 
    Category,
    COUNT(*) as total_orders,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as total_revenue,
    ROUND(AVG(`Purchase Amount (USD)`), 2) as avg_order_value,
    ROUND(AVG(`Review Rating`), 2) as avg_rating
FROM customer_shopping_data
GROUP BY Category
ORDER BY total_revenue DESC;

-- 2. Customer Segmentation by Season
SELECT 
    Season,
    COUNT(DISTINCT `Customer ID`) as unique_customers,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as total_sales,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage_of_total_sales
FROM customer_shopping_data
GROUP BY Season
ORDER BY total_sales DESC;

-- 3. The Impact of Discounts and Promo Codes on Total Revenue
SELECT 
    `Discount Applied`,
    COUNT(*) as total_transactions,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as total_revenue,
    ROUND(AVG(`Purchase Amount (USD)`), 2) as aov
FROM customer_shopping_data
GROUP BY `Discount Applied`;

-- 4. High-Value Customers (Top 10 By Lifetime Value proxy)
SELECT 
    `Customer ID`,
    Age,
    Gender,
    COUNT(*) as order_frequency,
    MAX(`Previous Purchases`) as historical_purchases,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as total_spend_this_year,
    `Subscription Status`
FROM customer_shopping_data
GROUP BY `Customer ID`, Age, Gender, `Subscription Status`
HAVING order_frequency > 1
ORDER BY total_spend_this_year DESC
LIMIT 10;

-- 5. Demographics Analysis: Spending Habits by Region and Age Group
WITH AgeGrouped AS (
    SELECT 
        `Customer ID`,
        CASE 
            WHEN Age BETWEEN 18 AND 24 THEN '18-24 (Gen Z)'
            WHEN Age BETWEEN 25 AND 34 THEN '25-34 (Millennials)'
            WHEN Age BETWEEN 35 AND 49 THEN '35-49 (Gen X)'
            ELSE '50+ (Boomers)'
        END AS age_group,
        Location,
        `Purchase Amount (USD)`
    FROM customer_shopping_data
)
SELECT 
    Location,
    age_group,
    COUNT(*) as total_purchases,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as net_spending
FROM AgeGrouped
GROUP BY Location, age_group
ORDER BY Location, net_spending DESC;

-- 6. Analyzing Shipping Type Efficiency by Payment Method
SELECT 
    `Shipping Type`,
    `Payment Method`,
    COUNT(*) as transaction_volume,
    ROUND(AVG(`Review Rating`), 2) as average_satisfaction_score
FROM customer_shopping_data
GROUP BY `Shipping Type`, `Payment Method`
ORDER BY `Shipping Type`, transaction_volume DESC;

-- 7. Monthly Sales Trend (Time Series Analysis)
-- (Assuming Purchase Date is stored in YYYY-MM-DD format as a string or Date object)
SELECT 
    SUBSTRING(`Purchase Date`, 1, 7) as purchase_month,
    COUNT(DISTINCT `Customer ID`) as active_customers,
    ROUND(SUM(`Purchase Amount (USD)`), 2) as monthly_revenue
FROM customer_shopping_data
GROUP BY SUBSTRING(`Purchase Date`, 1, 7)
ORDER BY purchase_month ASC;
