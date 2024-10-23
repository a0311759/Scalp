import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

def fetch_proxies():
    try:
        # URL of a public proxy list (modify this to match the source format)
        proxy_url = "https://www.free-proxy-list.net/"
        response = requests.get(proxy_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract proxies from the table
        proxy_list = []
        rows = soup.find("table", {"id": "proxylisttable"}).find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxy = f"http://{ip}:{port}"
                proxy_list.append(proxy)
        return proxy_list
    except Exception as e:
        st.error(f"Error fetching proxies: {e}")
        return []

def get_random_proxy(proxies):
    return {'http': random.choice(proxies), 'https': random.choice(proxies)}

def scrape_website(url, content_type, proxies):
    proxy = get_random_proxy(proxies)  # Get a random proxy from the list
    try:
        # Fetch the content from the URL using the selected proxy
        response = requests.get(url, proxies=proxy, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if content_type == 'html':
            return soup.prettify()  # Return the HTML content
        elif content_type == 'text':
            return soup.get_text(separator='\n', strip=True)  # Return plain text content
    except Exception as e:
        return f"Error: {e}"

# Fetch proxies once when the app starts
proxies = fetch_proxies()

# Streamlit user interface
st.title("Web Scraping Tool with Dynamic Proxies")

# Input field for the website URL
url = st.text_input("Enter the website address (URL):")

# Radio buttons for choosing content type
content_type = st.radio("Select content type:", ('html', 'text'))

# Submit button
if st.button("Scrape"):
    if url:
        if proxies:  # Check if proxies were successfully fetched
            result = scrape_website(url, content_type, proxies)
            st.text_area("Scraped Content:", result, height=300)
        else:
            st.error("No proxies available. Please try again later.")
    else:
        st.error("Please enter a valid URL.")

# Optional: Inform about rotating proxies
st.info("Proxies are rotated with each request for better anonymity.")
