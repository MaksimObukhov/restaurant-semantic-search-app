FROM python:3.11

WORKDIR /restaurant_search

COPY ./app/frontend ./app/frontend

RUN pip install --no-cache-dir --upgrade -r ./app/frontend/requirements.txt

COPY ./.env ./.env

CMD ["streamlit", "run", "app/frontend/streamlit_frontend.py", "--server.address=0.0.0.0", "--server.port=8501"]