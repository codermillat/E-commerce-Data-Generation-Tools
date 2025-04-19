# E-commerce Data Generation Tools

Python tools for generating and validating synthetic e-commerce order data with realistic customer behavior patterns.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ecommerce-data-generator.git
cd ecommerce-data-generator

# Install dependencies
pip install pandas numpy faker

# Generate dataset
python generate_ecommerce_data.py

# Validate dataset
python validate_and_clean_data.py
```

## 🛠️ Project Structure

```
ecommerce-data-generator/
│
├── generate_ecommerce_data.py    # Main data generation script
├── validate_and_clean_data.py    # Data validation and cleaning script
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## 📋 Requirements

- Python 3.8+
- pandas
- numpy
- Faker
- datetime
- uuid

## 🔧 Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Data Generation

```python
from generate_ecommerce_data import generate_customer_data, generate_dates, main

# Generate complete dataset
main()

# Or use individual components
customer_ids = generate_customer_data(num_customers=3000, num_orders=10000)
order_dates, shipping_dates = generate_dates(base_date=datetime.now(), num_orders=10000)
```

### Data Validation

```python
from validate_and_clean_data import validate_dataset, clean_dataset

# Validate existing dataset
df = pd.read_csv('ecommerce_orders_demo.csv')
issues = validate_dataset(df)

# Clean dataset
df_clean = clean_dataset(df)
```

## 📊 Features

### Data Generation (`generate_ecommerce_data.py`)

#### Main Functions

`generate_customer_data(num_customers, num_orders)`
- Generates customer IDs with realistic repeat patterns
- Arguments:
  - `num_customers`: Maximum number of unique customers
  - `num_orders`: Total number of orders to generate
- Returns: Array of customer IDs

`generate_dates(base_date, num_orders)`
- Generates order and shipping dates
- Arguments:
  - `base_date`: Reference date for order generation
  - `num_orders`: Number of date pairs to generate
- Returns: Tuple of (order_dates, shipping_dates)

`generate_address(faker)`
- Generates realistic addresses using Faker
- Arguments:
  - `faker`: Initialized Faker instance
- Returns: Formatted address string

### Data Validation (`validate_and_clean_data.py`)

#### Main Functions

`validate_dataset(df)`
- Performs comprehensive data validation
- Arguments:
  - `df`: pandas DataFrame to validate
- Returns: List of validation issues found

`clean_dataset(df)`
- Cleans dataset based on validation rules
- Arguments:
  - `df`: pandas DataFrame to clean
- Returns: Cleaned DataFrame

## 🧪 Testing

Run the validation script to test the generated data:

```bash
python validate_and_clean_data.py
```

This will:
1. Check for data quality issues
2. Validate value ranges and relationships
3. Generate a validation report
4. Create a cleaned dataset if issues are found

## 🔎 Data Generation Details

### Distributions

- Customer Orders: Power-law distribution
- Order Quantities: Poisson distribution (λ=2)
- Prices: Uniform distribution ($5-$500)
- Delivery Status: Weighted random distribution
- Dates: Uniform distribution within 12 months
- Shipping Delays: Uniform distribution (1-7 days)

### Customer Segmentation

- VIP: 5+ orders
- Returning: 2-4 orders
- New: 1 order

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a Pull Request

## 📝 Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Include docstrings for functions
- Add comments for complex logic

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Faker library for realistic address generation
- pandas and numpy for data manipulation
- All contributors to this project

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.
