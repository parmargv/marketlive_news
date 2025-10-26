import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="ET Markets News", layout="wide")

st.title("📰 Economic Times - Just Now Market News")

# Target URL
url = "https://economictimes.indiatimes.com/markets"
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the page
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the container for 'Just Now' news
container = soup.find("div", class_="FirstFoldWidget_scrollContainer__Ilb4S")

# Display headlines in rich format
if container:
    news_items = container.find_all("li")
    if news_items:
        st.markdown("### 🕒 Just Now Updates")
        for i, item in enumerate(news_items, start=1):
            headline_tag = item.find("a")
            if headline_tag:
                headline = headline_tag.get_text(strip=True)

                # Rich text display
                st.markdown(
                    f"""
<div style="
    background-color:#f8f9fa;
    padding:10px 15px;
    margin-bottom:8px;
    border-radius:10px;
    border-left:5px solid #2E86C1;
    font-size:16px;">
    <b>{i}. {headline}</b>
</div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("⚠️ No news items found in the container.")
else:
    st.error("❌ 'FirstFoldWidget_scrollContainer__Ilb4S' section not found.")






