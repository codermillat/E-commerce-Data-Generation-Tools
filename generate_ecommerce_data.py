import pandas as pd
import numpy as np
from faker import Faker
import uuid
from datetime import datetime, timedelta
import random

def generate_customer_data(num_customers, num_orders):
    """Generate customer IDs with realistic repeat patterns"""
    # Create a power-law distribution for customer frequency
    customer_ids = np.random.power(0.5, num_orders) * num_customers
    return np.clip(customer_ids.astype(int), 1, num_customers)

def generate_dates(base_date, num_orders):
    """Generate order and shipping dates within the last 12 months"""
    # Generate random order dates
    date_ranges = pd.date_range(end=base_date, periods=365, freq='D').to_pydatetime()
    order_dates = list(np.random.choice(date_ranges, size=num_orders))
    
    # Generate shipping dates (1-7 days after order)
    shipping_delays = np.random.randint(1, 8, size=num_orders)
    shipping_dates = [order_date + timedelta(days=int(delay)) 
                     for order_date, delay in zip(order_dates, shipping_delays)]
    
    return order_dates, shipping_dates

def generate_address(faker):
    """Generate a complete address string using Faker"""
    return f"{faker.street_address()}, {faker.city()}, {faker.state()} {faker.zipcode()}"

def determine_customer_segment(customer_frequencies):
    """Determine customer segment based on order frequency"""
    segments = []
    for freq in customer_frequencies:
        if freq >= 5:
            segments.append("VIP")
        elif freq >= 2:
            segments.append("Returning")
        else:
            segments.append("New")
    return segments

def main():
    # Initialize constants
    NUM_ORDERS = 10000
    NUM_CUSTOMERS = 3000
    NUM_PRODUCTS = 1000
    CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Beauty", "Toys"]
    DELIVERY_STATUS = {
        "Delivered": 0.70,
        "Shipped": 0.20,
        "Pending": 0.05,
        "Returned": 0.05
    }
    PAYMENT_METHODS = ["Credit Card", "PayPal", "Debit Card", "Apple Pay", "Google Pay"]
    DEVICE_TYPES = ["Desktop", "Mobile", "Tablet"]
    CHANNELS = ["Organic", "Paid Search", "Email", "Social"]

    # Initialize Faker
    fake = Faker()
    
    # Generate customer IDs with realistic repeat patterns
    customer_ids = generate_customer_data(NUM_CUSTOMERS, NUM_ORDERS)
    
    # Generate dates
    order_dates, shipping_dates = generate_dates(datetime.now(), NUM_ORDERS)
    
    # Create the main DataFrame
    df = pd.DataFrame({
        'order_id': [str(uuid.uuid4()) for _ in range(NUM_ORDERS)],
        'customer_id': customer_ids,
        'product_id': np.random.randint(1, NUM_PRODUCTS + 1, NUM_ORDERS),
        'category': np.random.choice(CATEGORIES, NUM_ORDERS),
        'price': np.round(np.random.uniform(5.0, 500.0, NUM_ORDERS), 2),
        'quantity': np.clip(np.random.poisson(2, NUM_ORDERS), 1, 10),
        'order_date': order_dates,
        'shipping_date': shipping_dates,
        'delivery_status': np.random.choice(
            list(DELIVERY_STATUS.keys()),
            NUM_ORDERS,
            p=list(DELIVERY_STATUS.values())
        ),
        'payment_method': np.random.choice(PAYMENT_METHODS, NUM_ORDERS),
        'device_type': np.random.choice(DEVICE_TYPES, NUM_ORDERS),
        'channel': np.random.choice(CHANNELS, NUM_ORDERS),
    })

    # Generate addresses
    df['shipping_address'] = [generate_address(fake) for _ in range(NUM_ORDERS)]
    df['billing_address'] = [generate_address(fake) for _ in range(NUM_ORDERS)]

    # Calculate customer segments based on frequency
    customer_frequencies = df['customer_id'].value_counts()
    df['customer_segment'] = df['customer_id'].map(
        lambda x: "VIP" if customer_frequencies[x] >= 5 
        else "Returning" if customer_frequencies[x] >= 2 
        else "New"
    )

    # Sort by order date
    df.sort_values('order_date', inplace=True)
    
    # Save to CSV
    df.to_csv('ecommerce_orders_demo.csv', index=False)
    print(f"Generated {NUM_ORDERS} orders for {len(df['customer_id'].unique())} unique customers")
    print(f"Data saved to ecommerce_orders_demo.csv")

if __name__ == "__main__":
    main()
