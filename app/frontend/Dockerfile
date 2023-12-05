FROM python:3.11

WORKDIR /restaurant_search

COPY ./app/frontend ./app/frontend

RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

COPY ./.env ./.env

CMD ["streamlit", "run", "app/frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]