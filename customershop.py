import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv(r"D:\excel\customershoppingbev\customer_shopping_behavior.csv")

# Display information (optional)
print(df.head())
print(df.info())

# Handle missing Review Rating values
df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.median())
)

# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Rename purchase amount column
df = df.rename(columns={
    'purchase_amount_(usd)': 'purchase_amount'
})

# Create age groups
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)

# Convert purchase frequency to days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(
    frequency_mapping
)

# PostgreSQL connection
username = "postgres"
password = "dfordatabase"
host = "localhost"
port = "5432"
database = "customer_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# Upload cleaned data
df.to_sql(
    'customer',
    engine,
    if_exists='replace',
    index=False
)

print("Data cleaned and uploaded successfully!")