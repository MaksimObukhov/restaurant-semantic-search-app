# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /restaurant_search

# Copy the requirements file into the container
COPY ./postgres/ ./postgres/

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r ./postgres/requirements.txt

# Copy the rest of the application code into the container
COPY ./data/businesses_postgres.csv ./data/businesses_postgres.csv
COPY ./data/reviews_postgres.csv ./data/reviews_postgres.csv
COPY ./.env /.env

# Command to run your application
CMD ["python", "postgres/postgres.py"]
