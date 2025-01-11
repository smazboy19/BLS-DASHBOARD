import streamlit as st
import requests
import pandas as pd

# Function to get BLS data using a valid API key and endpoint
def get_bls_data():
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN040010000000003?registrationKey=20c55f395a724712bd7c4f5dca5dc0cb"
    
    response = requests.get(url)
    
    # Print the raw response content for debugging
    if response.status_code == 200:
        st.write("Raw Response Data:")
        st.json(response.json())  # Display the raw JSON response for inspection
        return response.json()
    else:
        st.error("Failed to retrieve data from BLS API.")
        return None

# Function to process the raw data into a DataFrame
def process_data(data):
    try:
        # The raw data is inside 'Results' -> 'series' -> 'data'
        data_list = data['Results']['series'][0]['data']
        
        # Create a DataFrame
        df = pd.DataFrame(data_list)
        
        # Convert 'year' and 'period' to a proper date format
        df['date'] = df['year'] + "-" + df['period'].str[1:]
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Drop any rows with missing values
        df = df.dropna()
        
        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

# Function to display the dashboard
def display_dashboard():
    st.title("U.S. Bureau of Labor Statistics - Employment Data")

    # Fetch BLS data
    data = get_bls_data()

    if data:
        # Process and display the data
        df = process_data(data)
        
        if df is not None:
            st.subheader(f"Series: {data['Results']['series'][0]['seriesID']}")
            
            # Display the DataFrame
            st.write(df)
            
            # You can also plot the data over time
            st.line_chart(df.set_index('date')['value'])
        else:
            st.error("Failed to process data.")
    else:
        st.error("Failed to fetch data.")

# Run the dashboard
if __name__ == "__main__":
    display_dashboard()
