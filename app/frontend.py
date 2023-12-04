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
    # Display basic information
    restaurant_info = json_response["restaurant_info"]

    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Column 1: Display photo
    # Add your photo_url logic here
    photo_url = "https://5.imimg.com/data5/SELLER/Default/2020/9/JY/YB/UZ/5802447/restaurant-interior-designing-service-250x250.png"  # Replace with the actual photo URL
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
upload_business()
st.title("Elasticsearch Restaurant Search")

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
    if result:
        for i, hit in enumerate(result):
            display_restaurant_card(hit, i)
    else:
        st.write("No results found")
