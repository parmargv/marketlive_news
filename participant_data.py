import datetime
import streamlit as st
import urllib
import save_pdata
import pandas as pd
import pytz
import plotly.express as px
import plotly.graph_objects as go
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
                st.markdown(f'<h1 style="color:#319AA2 ;font-size:20px;">FII & PRO NET POSITION : {net_pos}</h1>',
                            unsafe_allow_html=True)
                st.table(df)
                col1 = ['client', 'DII', 'FII', 'PRO']
                CALL = [CLIENT_CALL, DII_CALL, FII_CALL, PRO_CALL]
                PUT = [CLIENT_PUT, DII_PUT, FII_PUT, PRO_PUT]
                NET = [CLIENT_NET, DII_NET, FII_NET, PRO_NET]
                # chart_data = pd.DataFrame(
                #     {"Client_Type": col1, "CALL": CALL, "PUT": PUT,"NET":NET}
                # )
                #
                # st.bar_chart(
                #     chart_data, x="Client_Type", y=["CALL","PUT","NET"], color=["#008000","#00ff00", "#ff0000"],height=600,width=1500,use_container_width=False
                # )

                option1 = st.selectbox(
                    'Save data?', ('NO', 'YES'))
                if option1 == "YES":
                    t2 = d.strftime("%d-%m-%Y")
                    FII_DATA = [t2, FII_CALL, FII_PUT, FII_NET]
                    PRO_DATA = [t2, PRO_CALL, PRO_PUT, PRO_NET]
                    DII_DATA = [t2, DII_CALL, DII_PUT, DII_NET]
                    CLI_DATA = [t2, CLIENT_CALL, CLIENT_PUT, CLIENT_NET]
                    NET = [t2, FII_NET + PRO_NET]
                    save_pdata.save_pro(FII_DATA, PRO_DATA, DII_DATA, CLI_DATA, NET)
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
def view_data():
    #st.set_page_config(page_title="Option Data Dashboard", layout="wide")

    # 📘 Load Excel file
    #excel_file = "p_data.xlsx"  # <-- replace with your actual Excel file name
    # sheets = ["FII", "DII", "PRO", "CLI","NET"]

    # df1 = data[0]
    # st.text("FII_OPTION_DATA")
    # st.bar_chart(df1.set_index('DATE'))
    # df2 = data[1]
    # st.text("PRO_OPTION_DATA")
    # st.bar_chart(df2.set_index('DATE'))
    # df3 = data[2]
    # st.text("NET_OPTION_DATA")
    # st.bar_chart(df3.set_index('DATE'))
    # df4 = data[3]
    # st.text("DII_OPTION_DATA")
    # st.bar_chart(df4.set_index('DATE'))
    # df5 = data[4]
    # st.text("CLI_OPTION_DATA")
    # st.bar_chart(df5.set_index('DATE'))
    data = save_pdata.read_data()
    st.title("📊 Option Data Dashboard")

    # Color mapping
    color_map = {"CALL": "green", "PUT": "red", "NET": "blue"}

    # Robust chart plotting function
    def plot_chart(df, title):
        df = df.copy()

        # Convert all numeric columns (except DATE)
        for col in df.columns:
            if col != "DATE":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        fig = go.Figure()

        # Plot each of CALL / PUT / NET if it exists
        for key in ["CALL", "PUT", "NET"]:
            # Match columns ending with key (handles prefixes)
            matching_cols = [c for c in df.columns if c.upper().endswith(key)]
            for col in matching_cols:
                fig.add_trace(go.Bar(
                    x=df["DATE"],
                    y=df[col],
                    name=key,
                    marker_color=color_map[key]
                ))

        # Layout
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Value",
            barmode="group",
            title_x=0.8,
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f9f9f9",
            font=dict(size=14),
            hovermode="x unified",
            legend=dict(title="Data Type", orientation="h", y=-0.2),
            xaxis = dict(
            tickfont=dict(size=14, family="Arial, sans-serif", color="black"),  # font size & color
            # title_font=dict(size=14, family="Arial, sans-serif", color="black"),  # title font size
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    # Display charts
    plot_chart(data[0], "📘 FII OPTION DATA")
    plot_chart(data[1], "📗 PRO OPTION DATA")
    plot_chart(data[2], "📙 NET OPTION DATA")  # Only DATE + NET will be plotted
    plot_chart(data[3], "📕 DII OPTION DATA")
    plot_chart(data[4], "📒 CLIENT OPTION DATA")