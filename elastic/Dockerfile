# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /restaurant_search

# Copy the requirements file into the container
COPY ./elastic/ ./elastic/

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r ./elastic/requirements.txt

# Copy the rest of the application code into the container
COPY ./data/reviews_elastic_sample.csv ./data/reviews_elastic_sample.csv

EXPOSE 8080

# Command to run your application
CMD ["uvicorn", "elastic.elastic:app", "--host", "0.0.0.0", "--port", "8080"]