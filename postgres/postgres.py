import os
from sqlalchemy import create_engine, MetaData, text, inspect
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# Database credentials
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
database = os.getenv('POSTGRES_DB')

# Create a connection string
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Create an SQLAlchemy engine
engine = create_engine(connection_string)
inspector = inspect(engine)

metadata = MetaData()

# Check if the table exists
if inspector.has_table('business_table', schema=database):
    # Drop the existing table
    with engine.connect() as connection:
        connection.execute(text(f'DROP TABLE IF EXISTS business_table'))

# Write the DataFrame to the PostgreSQL database
df_business = pd.read_csv('data/businesses_postgres.csv')
df_business.to_sql('business_table', engine, index=False, if_exists='replace')


# Repeat the process for the 'review_table'
if inspector.has_table('review_table', schema=database):
    with engine.connect() as connection:
        connection.execute(text(f'DROP TABLE IF EXISTS review_table'))

df_review = pd.read_csv('data/reviews_postgres.csv')
df_review.to_sql('review_table', engine, index=False, if_exists='replace')

