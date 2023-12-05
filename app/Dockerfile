FROM python:3.11

WORKDIR /restaurant_search

COPY ./app/db_upload ./app/db_upload
COPY ./app/routers ./app/routers
COPY ./app/main.py ./app/main.py
COPY ./app/requirements.txt ./app/requirements.txt

COPY ./data/businesses_postgres.csv ./data/businesses_postgres.csv
COPY ./data/reviews_elastic_sample.csv ./data/reviews_elastic_sample.csv

COPY ./.env ./.env

RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]