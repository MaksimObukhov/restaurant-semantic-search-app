import streamlit as st
import requests

# Elasticsearch server URL
API_URL = "http://elastic_py:8080"


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


def display_restaurant_card(json_response, acc):
    # # Display photo (if available)
    # photo_url = "https://example.com/restaurant-photo.jpg"  # Replace with the actual photo URL
    # st.image(photo_url, caption="Restaurant Photo", use_column_width=True)

    # Display basic information
    restaurant_info = json_response["restaurant_info"]
    st.markdown(f"## {acc + 1}. {restaurant_info['name']}")
    st.write(f"Categories: {restaurant_info['categories']}")
    st.write(f"Stars: {restaurant_info['stars']}")
    st.write(f"Review Count: {restaurant_info['review_count']}")
    st.write(f"Address: {restaurant_info['address']}")

    # Display working hours
    st.write("#### Working Hours")
    working_hours = {day.split(".")[1]: hours for day, hours in restaurant_info.items() if
                     day.startswith("WorkingHours")}
    for day, hours in working_hours.items():
        st.write(f"{day.capitalize()}: {hours}")


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
    st.title("Search Results:")
    result = search_businesses(search_query)
    st.write(result)
    # if result:
    #     for i, hit in enumerate(result):
    #         display_restaurant_card(hit, i)
    # else:
    #     st.write("No results found")
