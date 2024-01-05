import streamlit as st
import requests
import os

# Check if data has been uploaded
data_uploaded_flag_file = ".data_uploaded"
data_uploaded = os.path.exists(data_uploaded_flag_file)

# Server URL
ELASTIC_API_URL = "http://api:8080/elastic"
POSTGRES_API_URL = "http://api:8080/postgres"


# Function to upload data to Elasticsearch and PostgreSQL
def upload_data():
    try:
        # Check if data has been uploaded
        if not data_uploaded:
            url_el = f"{ELASTIC_API_URL}/upload_data"
            requests.post(url_el)

            url_pg = f"{POSTGRES_API_URL}/upload_data"
            requests.post(url_pg)

            # Create a flag file to indicate that data has been uploaded
            with open(data_uploaded_flag_file, "w") as flag_file:
                flag_file.write("Data uploaded")

            st.success("Data uploaded successfully to Elasticsearch and PostgreSQL")
        else:
            st.success("Data has already been uploaded")
    except Exception as e:
        st.write(str(e))


# Function to get business by ID from PostgreSQL
def get_postgres_business(business_id):
    url = f"{POSTGRES_API_URL}/get_business/{business_id}"
    response = requests.get(url)
    return response.json()


# Function to search businesses in Elasticsearch
def search_elastic_businesses(query):
    url = f"{ELASTIC_API_URL}/search_elastic/{query}"
    response = requests.get(url)
    return response.json()


def match_elastic_businesses(response_list):
    for business in response_list:
        business['restaurant_info'] = get_postgres_business(business['business_id'])
    return response_list


# Display restaurant card
def display_restaurant_card(json_response, acc):
    # Display basic information
    restaurant_info = json_response["restaurant_info"]

    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Column 1: Display photo
    # Add your photo_url logic here
    photo_url = "https://t3.ftcdn.net/jpg/03/24/73/92/360_F_324739203_keeq8udvv0P2h1MLYJ0GLSlTBagoXS48.jpg"
    col1.image(photo_url, use_column_width=True)

    # Column 2: Display information
    col2.markdown(f"## {acc + 1}. {restaurant_info['name']}")
    col2.write(f"**Categories:** {restaurant_info['categories']}")
    col2.write(f"**Stars:** {restaurant_info['stars']}")
    col2.write(f"**Review Count:** {restaurant_info['review_count']}")
    col2.write(f"**Address:** {restaurant_info['address']}")

    # Column 3: Display working hours
    col3.write("#### Working Hours")
    working_hours = {day.split(".")[1]: hours for day, hours in restaurant_info.items() if
                     day.startswith("WorkingHours")}
    if all(value == "closed" for value in working_hours.values()):
        col3.write("No Information")
    else:
        for day, hours in working_hours.items():
            col3.write(f"**{day.capitalize()}:** {hours}")


# Automatically upload data at start
upload_data()

# Title with Description
st.title("Restaurants of Philadelphia")
st.markdown("### Describe your desired restaurant and we will find it!")

# Create the text input with JavaScript event handlers
search_query = st.text_input("Today I'll have...", value="Cozy Italian trattoria with outdoor seating", max_chars=100, key="search_query")

if st.button("Search"):
    st.title("Restaurants:")
    result = search_elastic_businesses(search_query)
    if result:
        result = match_elastic_businesses(result)
        for i, hit in enumerate(result):
            display_restaurant_card(hit, i)
    else:
        st.write("No results found")

