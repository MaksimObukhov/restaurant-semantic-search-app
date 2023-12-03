# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /restaurant_search

# Copy the requirements file into the container
COPY ./app/ ./app/

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

CMD ["streamlit", "run", "app/frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]