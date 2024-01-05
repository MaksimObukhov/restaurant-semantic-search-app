# Philadelphia Restaurant Search Application

## Description

This project is a search application that uses Elasticsearch and PostgreSQL to provide restaurant recommendations based on user queries. The application is built with Python and uses the Streamlit library for the frontend and FastAPI for the backend. Containerized with Docker.

## Features

- Upload data to Elasticsearch and PostgreSQL.
- Search for restaurants based on user queries.
- Display restaurant information including name, categories, stars, review count, address, and working hours.

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
```
2. Navigate to the project directory:
```bash
cd <project_directory>
```
3. Build the Docker images:
```bash
docker-compose build
```

## Usage

1. Start the application:
```bash
docker-compose up
```
2. Open a web browser and navigate to `http://localhost:8501`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
