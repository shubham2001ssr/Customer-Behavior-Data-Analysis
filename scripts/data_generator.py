import csv
import random
from datetime import datetime, timedelta
import os

def generate_mock_data(num_records=5000):
    gender_opts = ['Male', 'Female']
    items = ['Sweater', 'Jeans', 'Sneakers', 'T-shirt', 'Jacket', 'Sunglasses', 'Backpack', 'Hat', 'Dress', 'Shorts', 'Scarf', 'Belt']
    categories = ['Clothing', 'Clothing', 'Shoes', 'Clothing', 'Outerwear', 'Accessories', 'Accessories', 'Accessories', 'Clothing', 'Clothing', 'Accessories', 'Accessories']
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    sizes = ['S', 'M', 'L', 'XL']
    colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Grey', 'Brown']
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    shipping_types = ['Standard', 'Express', 'Next Day', 'Store Pickup']
    payment_methods = ['Credit Card', 'PayPal', 'Cash', 'Debit Card', 'Apple Pay']
    
    start_date = datetime(2023, 1, 1)
    
    data = []
    
    for i in range(1, num_records + 1):
        customer_id = random.randint(1000, 2500)
        age = random.randint(18, 70)
        gender = random.choices(gender_opts, weights=[0.48, 0.52])[0]
        
        item_idx = random.randint(0, len(items)-1)
        item_purchased = items[item_idx]
        category = categories[item_idx]
        
        purchase_amount = round(random.uniform(20.0, 300.0), 2)
        location = random.choice(locations)
        size = random.choice(sizes)
        color = random.choice(colors)
        season = random.choice(seasons)
        review_rating = round(random.uniform(1.0, 5.0), 1)
        subscription_status = random.choices(['Yes', 'No'], weights=[0.3, 0.7])[0]
        shipping_type = random.choice(shipping_types)
        discount_applied = random.choices(['Yes', 'No'], weights=[0.4, 0.6])[0]
        promo_code = 'Yes' if discount_applied == 'Yes' else 'No'
        previous_purchases = random.randint(0, 50)
        payment_method = random.choice(payment_methods)
        freq_of_purchases = random.choice(['Weekly', 'Bi-Weekly', 'Monthly', 'Every 3 Months', 'Annually'])
        
        days_offset = random.randint(0, 365)
        purchase_date = start_date + timedelta(days=days_offset)
        
        data.append([
            customer_id, age, gender, item_purchased, category, purchase_amount, location, size, color, season,
            review_rating, subscription_status, shipping_type, discount_applied, promo_code, previous_purchases,
            payment_method, freq_of_purchases, purchase_date.strftime('%Y-%m-%d')
        ])
        
    os.makedirs('data', exist_ok=True)
    with open('data/customer_shopping_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Customer ID', 'Age', 'Gender', 'Item Purchased', 'Category', 'Purchase Amount (USD)', 'Location',
            'Size', 'Color', 'Season', 'Review Rating', 'Subscription Status', 'Shipping Type', 'Discount Applied',
            'Promo Code Used', 'Previous Purchases', 'Payment Method', 'Frequency of Purchases', 'Purchase Date'
        ])
        writer.writerows(data)
    print("Mock dataset generated successfully at data/customer_shopping_data.csv")

if __name__ == "__main__":
    generate_mock_data()
