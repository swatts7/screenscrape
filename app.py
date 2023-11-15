import streamlit as st
from bs4 import BeautifulSoup
import requests
import base64

def fetch_and_clean_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted tags
    for tag in soup(['script', 'nav', 'style', 'footer', 'header', 'form']):
        tag.decompose()

    # Remove 'id' and 'class' attributes from the desired tags
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']):
        for attribute in ["class", "id"]:
            del tag[attribute]

    # Combine the remaining tags into a single string
    clean_html = ''.join(str(tag) for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']))
    return clean_html

def get_screenshot(url, api_key):
    API_ENDPOINT = "http://api.screenshotlayer.com/api/capture"

    params = {
        "access_key": api_key,
        "url": url,
        "fullpage": 1,
        "viewport": "1440x900"  # You can adjust this as needed
    }

    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.content
    else:
        return None

def main():
    st.title("Webpage Scraper and Screenshot Tool")

    url = st.text_input("Enter the URL of the webpage")
    api_key = "78a7ba1fd66399e0defa9bb3abebe06e"  # Replace with your actual API key

    if st.button("Process"):
        if url:
            with st.spinner('Fetching and processing webpage...'):
                clean_html = fetch_and_clean_html(url)
                screenshot = get_screenshot(url, api_key)

                st.subheader("Processed HTML")
                st.text_area("Clean HTML", clean_html, height=300)

                if screenshot:
                    st.subheader("Webpage Screenshot")
                    st.image(screenshot, caption='Full Page Screenshot', use_column_width=True)

                    # Convert screenshot to base64 for easy copying
                else:
                    st.error("Unable to capture screenshot")
        else:
            st.error("Please enter a URL")

if __name__ == "__main__":
    main()