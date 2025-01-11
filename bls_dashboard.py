import streamlit as st
import requests
import json
import pandas as pd

# Set your BLS API key here
API_KEY = '20c55f395a724712bd7c4f5dca5dc0cb'

# Function to get the latest BLS data using API
def get_bls_data():
    # Set the URL to query the API
    url = f'https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN040010000000003?registrationKey={API_KEY}'
    response = requests.get(url)
    
    # If the response is valid, load the data
    if response.status_code == 200:
        data = response.json()
        
        # Extracting the data we need (time series data)
        series_data = data['Results']['series'][0]['data']
        
        # Creating a DataFrame to display the data
        df = pd.DataFrame(series_data)
        
        # Convert the "year", "period", and "value" columns to appropriate types
        df['year'] = df['year'].astype(int)
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['period'] = df['period'].str.slice(1)
        df['period_name'] = df['period'].apply(lambda x: {
            'M01': 'January', 'M02': 'February', 'M03': 'March',
            'M04': 'April', 'M05': 'May', 'M06': 'June',
            'M07': 'July', 'M08': 'August', 'M09': 'September',
            'M10': 'October', 'M11': 'November', 'M12': 'December'
        }.get(x, 'Unknown'))
        
        return df
    else:
        st.error("Error fetching data from BLS API")
        return None

# Streamlit app layout
st.title('U.S. Bureau of Labor Statistics - Employment Data')
st.write('This dashboard displays the latest U.S. employment data based on BLS API.')

# Fetch and display data
df = get_bls_data()

if df is not None:
    st.subheader("Latest Employment Data")
    st.write(df)
