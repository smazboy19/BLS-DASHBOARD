import streamlit as st
import requests

# Function to get BLS data using a valid API key and endpoint
def get_bls_data():
    # Replace with your actual API key
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN040010000000003?registrationKey=20c55f395a724712bd7c4f5dca5dc0cb"
    
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to retrieve data from BLS API.")
        return None

# Function to display the dashboard
def display_dashboard():
    st.title("U.S. Bureau of Labor Statistics - Employment Data")

    # Fetch BLS data
    data = get_bls_data()

    if data:
        # Extracting the data we want to display
        if 'Results' in data and 'series' in data['Results']:
            series = data['Results']['series'][0]
            st.subheader("Series Title: " + series['seriesID'])
            st.write("Data: ", series['data'])
        else:
            st.error("No data found.")
    else:
        st.error("Failed to fetch data.")

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
