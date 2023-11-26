import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, ForeignKey, Float
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
database = os.getenv('POSTGRES_DBNAME')

# Create a connection string
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

metadata = MetaData()

# Define your table structure
business_table = Table(
    'business_table',
    metadata,
    Column('business_id', Integer, primary_key=True),
    Column('name', String),
    Column('address', String),
    Column('postal_code', String),
    Column('stars', Float),
    Column('review_count', Integer),
    Column('categories', String),
    Column('working_hours_monday', String),
    Column('working_hours_tuesday', String),
    Column('working_hours_wednesday', String),
    Column('working_hours_thursday', String),
    Column('working_hours_friday', String),
    Column('working_hours_saturday', String),
    Column('working_hours_sunday', String)
)

review_table = Table(
    'review_table',
    metadata,
    Column('review_id', Integer, primary_key=True),
    Column('business_id', Integer, ForeignKey('business_table.business_id')),
    Column('stars', Float),
    Column('useful', Integer),
    Column('funny', Integer),
    Column('cool', Integer),
    Column('text', String)
)
# Create the table
metadata.create_all(engine)

# Write the DataFrame to the PostgreSQL database
df_business = pd.read_csv('data/businesses_postgres.csv')
df_business.to_sql('business_table', engine, index=False, if_exists='replace')

df_review = pd.read_csv('data/reviews_postgres.csv')
df_review.to_sql('review_table', engine, index=False, if_exists='replace')


