import streamlit as st
import requests

# Elasticsearch server URL
ELASTICSEARCH_URL = "http://localhost:8000"

index_name = 'restaurant_search'

def add_business(business_id):
    url = f"{ELASTICSEARCH_URL}/{index_name}/add"
    data = {"business_id": business_id}
    response = requests.post(url, json=data)
    return response.json()


def get_business(business_id):
    url = f"{ELASTICSEARCH_URL}/{index_name}/{business_id}"
    response = requests.get(url)
    return response.json()


def search_businesses(query):
    url = f"{ELASTICSEARCH_URL}/{index_name}/search?query={query}"
    response = requests.get(url)
    return response.json()


st.title("Elasticsearch Restaurant Search")

# Add Business Form
st.header("Add Business")
business_id = st.text_input("Business ID")
if st.button("Add Business"):
    result = add_business(business_id)
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
