import streamlit as st
import requests

# Elasticsearch server URL
API_URL = "http://elastic_py:8080"


# API_URL = "http://0.0.0.0:8080"


def upload_business():
    url = f"{API_URL}/upload_data"
    response = requests.post(url)
    return response.json()


def get_business(business_id):
    url = f"{API_URL}/{business_id}"
    response = requests.get(url)
    return response.json()


def search_businesses(query):
    url = f"{API_URL}/search/{query}"
    response = requests.get(url)
    return response.json()


def health_check():
    url = f"{API_URL}/health"
    response = requests.get(url)
    return response.json()


st.title("Elasticsearch Restaurant Search")

# Add Business Form
st.header("Upload Data")
if st.button("Upload"):
    result = upload_business()
    st.success(result["message"])

# Get Business by ID
st.header("Get Business by ID")
business_id_to_get = st.text_input("Enter Business ID to Retrieve")
if st.button("Get Business"):
    result = get_business(business_id_to_get)
    st.write(result)

# Search Businesses
st.header("Search Businesses")
search_query = st.text_input("Enter Search Query")
if st.button("Search"):
    result = search_businesses(search_query)
    st.write(result)
