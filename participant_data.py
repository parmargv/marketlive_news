import datetime
import urllib
import save_pdata
import pytz
from supabase import create_client, Client
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np   # ← add this line
def fetch_data():
    user_id = st.text_input('Enter userId:')
    user_pw = st.text_input('Enter password:')
    india_timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(india_timezone).time()
    USER_ID="gvparmar"
    USER_PW="Gvp@123"
    option1 = st.selectbox('Are you sure?', ('N', 'Y'))
    if option1 == "Y":
        if user_id == USER_ID and user_pw == USER_PW:
            d = st.date_input("Enter Date", datetime.date(2024, 6, 28))
            st.write('Selected Date is:', d)
            option = st.selectbox(
                'Date is ok?', ('NO', 'YES'))
            if option == "YES":
                t = d.strftime("%d%m%Y")
                url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_" + str(t) + ".csv"

                headers = {}
                headers[
                    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
                req = urllib.request.Request(url, headers=headers)
                resp = urllib.request.urlopen(req)
                df = pd.read_csv(f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_" + str(t) + ".csv",
                                 skiprows=1)
                pd.set_option('display.max_columns', None)

                df2 = df.T
                df2.index = df2.index.str.strip()
                df2.loc['Future index'] = df2.loc['Future Index Long'] - df2.loc['Future Index Short']
                df2.loc['Future stock'] = df2.loc['Future Stock Long'] - df2.loc['Future Stock Short']
                df2.loc['Index call'] = df2.loc['Option Index Call Long'] - df2.loc['Option Index Call Short']
                df2.loc['Index put'] = df2.loc['Option Index Put Long'] - df2.loc['Option Index Put Short']
                df2.loc['Stock call'] = df2.loc['Option Stock Call Long'] - df2.loc['Option Stock Call Short']
                df2.loc['Stock put'] = df2.loc['Option Stock Put Long'] - df2.loc['Option Stock Put Short']
                df2.loc['Net Option position'] = df2.loc['Index call'] - df2.loc['Index put']

                first_7_rows = df2.head(1)
                last_7_rows = df2.tail(7)
                df = pd.concat([first_7_rows, last_7_rows])
                df = df.drop(df.columns[-1], axis=1)
                net_pos = int(df.iloc[7, 2]) + int(df.iloc[7, 3])
                CLIENT_CALL = df.iloc[3, 0]
                CLIENT_PUT = df.iloc[4, 0]
                CLIENT_NET = df.iloc[7, 0]
                DII_CALL = df.iloc[3, 1]
                DII_PUT = df.iloc[4, 1]
                DII_NET = df.iloc[7, 1]
                FII_CALL = df.iloc[3, 2]
                FII_PUT = df.iloc[4, 2]
                FII_NET = df.iloc[7, 2]
                PRO_CALL = df.iloc[3, 3]
                PRO_PUT = df.iloc[4, 3]
                PRO_NET = df.iloc[7, 3]
                st.markdown(f'<h1 style="color:#319AA2 ;font-size:20px;">FII & PRO NET POSITION : {net_pos}</h1>',unsafe_allow_html=True)
                st.table(df)
                col1 = ['client', 'DII', 'FII', 'PRO']
                CALL = [CLIENT_CALL, DII_CALL, FII_CALL, PRO_CALL]
                PUT = [CLIENT_PUT, DII_PUT, FII_PUT, PRO_PUT]
                NET = [CLIENT_NET, DII_NET, FII_NET, PRO_NET]


                option1 = st.selectbox('Save data?', ('NO', 'YES'))
                if option1 == "YES":
                    url = "https://cdxnmcpozkfdiqjsthqs.supabase.co"
                    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5tY3BvemtmZGlxanN0aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMTk1NzEsImV4cCI6MjA3Nzg5NTU3MX0.wQing-u7lKbYQgXeDvTsTzT5zXVv8Q5Jg1_91PdJxmo"
                    supabase = create_client(url, key)
                    t2 = d.strftime("%Y-%m-%d")
                    FII_DATA ={
                        "DATE": t2,
                        "FII_CALL": FII_CALL,
                        "FII_PUT": FII_PUT,
                        "FII_NET": FII_NET
                    }

                    PRO_DATA = {
                        "DATE": t2,
                        "PRO_CALL": PRO_CALL,
                        "PRO_PUT": PRO_PUT,
                        "PRO_NET": PRO_NET
                    }

                    DII_DATA = {
                        "DATE": t2,
                        "DII_CALL": DII_CALL,
                        "DII_PUT": DII_PUT,
                        "DII_NET": DII_NET
                    }
                    CLI_DATA = {
                        "DATE": t2,
                        "CLI_CALL": CLIENT_CALL,
                        "CLI_PUT": CLIENT_PUT,
                        "CLI_NET": CLIENT_NET
                    }
                    NET_DATA = {
                    "DATE": t2,
                    "FII_NET": FII_NET,
                    "PRO_NET": PRO_NET
                    }

                    response = supabase.table("fii_data").insert(FII_DATA).execute()
                    response = supabase.table("dii_data").insert(DII_DATA).execute()
                    response = supabase.table("pro_data").insert(PRO_DATA).execute()
                    response = supabase.table("cli_data").insert(CLI_DATA).execute()
                    response = supabase.table("net_data").insert(NET_DATA).execute()

                    st.write('Data saved.....')
                else:
                    st.write('not saved')
                option2 = st.selectbox(
                    'Clear data?', ('NO', 'YES'))
                if option2 == "YES":
                    save_pdata.clear_data()
                    st.write('Data cleared.....')
                else:
                    st.write('Data not clear')
def get_data(indices):
    url = "https://cdxnmcpozkfdiqjsthqs.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5tY3BvemtmZGlxanN0aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMTk1NzEsImV4cCI6MjA3Nzg5NTU3MX0.wQing-u7lKbYQgXeDvTsTzT5zXVv8Q5Jg1_91PdJxmo"
    supabase = create_client(url, key)
    if indices == "FII":
        response = supabase.table("fii_data").select("*").execute()
    elif indices == "PRO":
        response = supabase.table("pro_data").select("*").execute()
    elif indices == "DII":
        response = supabase.table("dii_data").select("*").execute()
    elif indices == "CLI":
        response = supabase.table("cli_data").select("*").execute()
    elif indices == "NET":
        response = supabase.table("net_data").select("*").execute()

    df = pd.DataFrame(response.data)
    # df['buy_t'] = pd.to_datetime(df['buy_t']).dt.strftime('%Y-%m-%d %H:%M')
    # df['sell_t'] = pd.to_datetime(df['sell_t']).dt.strftime('%Y-%m-%d %H:%M')
    return df
def view_data(ans):
    st.title("📊 Option Data Dashboard")
    df = get_data(ans)

    # Dropdown to select which data to view
    selection = st.selectbox("Select Data Type", ["CALL", "PUT", "NET"])

    # Color mapping
    color_map = {"CALL": "green", "PUT": "red", "NET": "blue"}

    def plot_chart(df, title, selection):
        df = df.copy()

        # Convert numeric columns
        for col in df.columns:
            if col != "DATE":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        fig = go.Figure()

        # Plot only selected data (columns ending with selection)
        matching_cols = [c for c in df.columns if c.upper().endswith(selection)]
        for col in matching_cols:
            fig.add_trace(go.Bar(
                x=df["DATE"],
                y=df[col],
                name=selection,
                marker_color=color_map[selection]
            ))

        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Value",
            barmode="group",
            title_x=0.5,
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f9f9f9",
            font=dict(size=14),
            hovermode="x unified",
            legend=dict(title="Data Type", orientation="h", y=-0.2),
            xaxis=dict(
                tickfont=dict(size=14, family="Arial, sans-serif", color="black"),
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    # Display selected chart
    plot_chart(df, f"📘 OPTION DATA - {selection}", selection)