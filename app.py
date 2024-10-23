import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_website(url, content_type):
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if content_type == 'html':
            return soup.prettify()  # Return the HTML content
        elif content_type == 'text':
            return soup.get_text(separator='\n', strip=True)  # Return plain text content
    except Exception as e:
        return f"Error: {e}"

# Streamlit user interface
st.title("Web Scraping Tool")

# Input field for the website URL
url = st.text_input("Enter the website address (URL):")

# Radio buttons for choosing content type
content_type = st.radio("Select content type:", ('html', 'text'))

# Submit button
if st.button("Scrape"):
    if url:
        result = scrape_website(url, content_type)
        st.text_area("Scraped Content:", result, height=300)
    else:
        st.error("Please enter a valid URL.")
