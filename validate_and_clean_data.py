import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

def validate_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def validate_dataset(df):
    """Perform all validation checks and return issues found"""
    issues = []
    
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        issues.append(f"Found null values: {null_counts[null_counts > 0].to_dict()}")

    # Validate ranges
    if not df['customer_id'].between(1, 3000).all():
        issues.append("Found customer_ids outside valid range (1-3000)")
    
    if not df['product_id'].between(1, 1000).all():
        issues.append("Found product_ids outside valid range (1-1000)")
    
    if not df['price'].between(5.0, 500.0).all():
        issues.append("Found prices outside valid range (5.0-500.0)")
    
    if not df['quantity'].between(1, 10).all():
        issues.append("Found quantities outside valid range (1-10)")

    # Validate categorical values
    valid_categories = {"Electronics", "Clothing", "Home", "Books", "Beauty", "Toys"}
    invalid_categories = set(df['category'].unique()) - valid_categories
    if invalid_categories:
        issues.append(f"Found invalid categories: {invalid_categories}")

    valid_delivery_status = {"Pending", "Shipped", "Delivered", "Returned"}
    invalid_status = set(df['delivery_status'].unique()) - valid_delivery_status
    if invalid_status:
        issues.append(f"Found invalid delivery status: {invalid_status}")

    valid_payment_methods = {"Credit Card", "PayPal", "Debit Card", "Apple Pay", "Google Pay"}
    invalid_payments = set(df['payment_method'].unique()) - valid_payment_methods
    if invalid_payments:
        issues.append(f"Found invalid payment methods: {invalid_payments}")

    # Check for duplicate order_ids
    duplicate_orders = df[df['order_id'].duplicated()]
    if not duplicate_orders.empty:
        issues.append(f"Found {len(duplicate_orders)} duplicate order_ids")

    # Validate UUIDs
    invalid_uuids = df[~df['order_id'].apply(validate_uuid)]
    if not invalid_uuids.empty:
        issues.append(f"Found {len(invalid_uuids)} invalid UUIDs")

    # Check date consistency
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['shipping_date'] = pd.to_datetime(df['shipping_date'])
    invalid_dates = df[df['shipping_date'] <= df['order_date']]
    if not invalid_dates.empty:
        issues.append(f"Found {len(invalid_dates)} orders with shipping_date <= order_date")

    # Check shipping delay range
    shipping_delays = (df['shipping_date'] - df['order_date']).dt.days
    invalid_delays = df[~shipping_delays.between(1, 7)]
    if not invalid_delays.empty:
        issues.append(f"Found {len(invalid_delays)} orders with shipping delays outside 1-7 days")

    return issues

def clean_dataset(df):
    """Clean the dataset based on validation rules"""
    print("Initial shape:", df.shape)
    
    # Remove rows with null values
    df = df.dropna()
    
    # Remove rows with invalid ranges
    df = df[
        df['customer_id'].between(1, 3000) &
        df['product_id'].between(1, 1000) &
        df['price'].between(5.0, 500.0) &
        df['quantity'].between(1, 10)
    ]
    
    # Remove rows with invalid categories
    valid_categories = {"Electronics", "Clothing", "Home", "Books", "Beauty", "Toys"}
    df = df[df['category'].isin(valid_categories)]
    
    # Remove rows with invalid delivery status
    valid_delivery_status = {"Pending", "Shipped", "Delivered", "Returned"}
    df = df[df['delivery_status'].isin(valid_delivery_status)]
    
    # Remove rows with invalid payment methods
    valid_payment_methods = {"Credit Card", "PayPal", "Debit Card", "Apple Pay", "Google Pay"}
    df = df[df['payment_method'].isin(valid_payment_methods)]
    
    # Remove duplicate order_ids
    df = df.drop_duplicates(subset=['order_id'])
    
    # Remove orders with invalid dates
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['shipping_date'] = pd.to_datetime(df['shipping_date'])
    df = df[df['shipping_date'] > df['order_date']]
    
    # Remove orders with invalid shipping delays
    shipping_delays = (df['shipping_date'] - df['order_date']).dt.days
    df = df[shipping_delays.between(1, 7)]
    
    print("Final shape:", df.shape)
    return df

def main():
    # Read the dataset
    df = pd.read_csv('ecommerce_orders_demo.csv')
    print("Loading dataset...")
    
    # Validate the dataset
    print("\nValidating dataset...")
    issues = validate_dataset(df)
    if issues:
        print("\nFound the following issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues found in the dataset!")
    
    # Clean the dataset
    print("\nCleaning dataset...")
    df_clean = clean_dataset(df)
    
    # Save cleaned dataset
    output_file = 'ecommerce_orders_clean.csv'
    df_clean.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to {output_file}")
    print(f"Removed {len(df) - len(df_clean)} problematic records")

if __name__ == "__main__":
    main()
