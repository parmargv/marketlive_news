import News
import participant_data
import supabase_read
import world_market
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import datetime
from datetime import date
import working_day
import requests
from bs4 import BeautifulSoup
import oi_data
from datetime import datetime, time
import pytz

def plot_graph():
    st_autorefresh(interval=60 * 1000, key="dataframerefresh")
    oi_data.plot_pcr()
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    st_time = time(15, 30)
    if now >= st_time:
        main()
def save_pre_data():
    st.write("Saving previous day data....")
    df = supabase_read.fetch_pcr_from_supabase("NIFTY",limit=120)
    ce_oi = int(df['net_ce_oi'].iloc[0])
    pe_oi = int(df['net_pe_oi'].iloc[0])
    supabase_read.update_pre_data(ce_oi,pe_oi)
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    st_time = time(9, 12)
    if now >= st_time:
        main()


def clear_data():
    st_autorefresh(interval=60 * 1000, key="dataframerefresh")
    st.write("PCR DATA CLEARED....")
    supabase_read.clear()
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    st_time = time(9, 15)
    if now >= st_time:
        main()

def off_market():
    st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    india_timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india_timezone).time()
    today = date.today()

    #st.markdown(f'<marquee behavior="scroll" direction="left">Current_Time:{formatted_time},Today:-{today_name},Login_state:-{login_state},User_Name:{user_name}</marquee>', unsafe_allow_html=True)

    activity = ['Home','News','Gainer_Looser_future','World_market','PCR_CHART','OI_DATA','FII_data','Participant_data','View_Particpant _Data']
    choice = st.sidebar.selectbox("Main Menu", activity)

    if choice == "Home":

        st_autorefresh(interval=30 * 1000, key="dataframerefresh")
        st.markdown(f'<h1 style="color:#319AA2 ;font-size:25px;">Welcome to live market news and data.....</h1>',unsafe_allow_html=True)
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
                                font-size:16px;
                            ">
                                <span style="color:#E64D27; font-weight:bold;">
                                    {i}. {headline}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning("⚠️ No news items found in the container.")
        else:
            st.error("❌ 'FirstFoldWidget_scrollContainer__Ilb4S' section not found.")
        st.balloons()

    if choice=="News":
        News.get_data()

    if choice == "PCR_CHART":
        oi_data.plot_pcr()

    if choice =="OI_DATA":
        oi_data.plot_chart()

    if choice == "Gainer_Looser_future":
        st_autorefresh(interval=60 * 1000, key="dataframerefresh")
        world_market.gainer_looser_fo()

    if choice=="World_market":
        df3=world_market.groww_data()
        st.table(df3)
    if choice=='FII_data':
        df = world_market.cash()
        hide_table_row_index = """
                                                                                <style>
                                                                                tbody th {display:none}
                                                                                .blank {display:none}
                                                                                </style>
                                                                                """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df)
    if choice=='Participant_data':
        participant_data.fetch_data()

    if choice == "View_Particpant _Data":
        option1 = st.selectbox('Select the Participant?', ('FII','PRO','CLIENT','DII','NET'))
        if option1 == "FII":
            ans = "FII"
        elif option1 == "PRO":
            ans = "PRO"
        elif option1 == "CLIENT":
            ans = "CLI"
        elif option1 == "DII":
            ans = "DII"
        elif option1 == "NET":
            ans = "NET"
        else:
            ans = "NO"

        option2 = st.selectbox('Are you sure??', ('N','Y'))
        if option2 == "Y":
            participant_data.view_data(ans)

def main():
    today = date.today()
    to_day = working_day.is_working_day(today)
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india).time()
    save_pcr = time(9, 10)
    clear_pcr = time(9, 12)
    market_start = time(9, 15)
    market_end = time(15, 30)

    if clear_pcr > now >= save_pcr:
       save_pre_data()
    elif market_start > now >= clear_pcr:
        clear_data()
    elif market_start <= now <= market_end:
        plot_graph()
    else:
        off_market()
if __name__ == "__main__":
    main()