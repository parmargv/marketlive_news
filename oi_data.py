import streamlit as st
import pandas as pd
import pytz
import trade_all
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
from streamlit_autorefresh import st_autorefresh
import time
import supabase_read

# ================= CONFIG =================
TOKEN_FILE = "token.txt"
DATA_FILE = "oi_history.csv"
SYMBOL = "NSE:NIFTY50-INDEX"
TIMEZONE = pytz.timezone("Asia/Kolkata")
# =========================================

#st.set_page_config(page_title="Live OI Chart", layout="wide")


def get_token():
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()


def fetch_oi(token, symbol):
    data = trade_all.o_chain(token, symbol)
    return data
    # return pd.DataFrame({
    #     "OI_DIFF": [data["OI_DIFF"].iloc[2]]
    # })


def get_timestamp():
    return datetime.now(TIMEZONE).replace(second=0, microsecond=0)


def save_data(df):
    if os.path.exists(DATA_FILE):
        hist = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
    else:
        hist = pd.DataFrame()

    hist = pd.concat([hist, df], ignore_index=True)
    hist.drop_duplicates(subset=["timestamp"], keep="last", inplace=True)
    hist.to_csv(DATA_FILE, index=False)

    return hist


# 🔁 Auto refresh every 1 minute
#st_autorefresh(interval=60_000, key="oi_refresh")
#st_autorefresh(interval=20 * 1000, key="dataframe refresh_5")
# st.title("📊 Live OI Difference Chart")
#
# token = get_token()
#
# df = fetch_oi(token, SYMBOL)
# ts = get_timestamp()
# df["timestamp"] = ts
# df["timestamp_str"] = ts.strftime("%Y-%m-%d %H:%M")
#
# history = save_data(df)
#
# # 📈 Plot live chart
# history["timestamp"] = pd.to_datetime(
#     history["timestamp"],
#     errors="coerce"
# )
#
# # 2. Remove timezone info ONLY (keep IST clock time)
# history["timestamp"] = history["timestamp"].apply(
#     lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x
# )
#
# # 3. Sort and plot
# history = history.sort_values("timestamp")
# history.set_index("timestamp", inplace=True)
#
# st.line_chart(history["OI_DIFF"])
def plot_chart():
    st_autorefresh(interval=60 * 1000, key="dataframe refresh_5")
    token = supabase_read.get_token()
    df = fetch_oi(token, "NSE:NIFTY50-INDEX")

    # =========================
    # Common Settings
    # =========================
    x_labels = df["strike_price"].astype(str)
    x = np.arange(len(x_labels))
    width = 0.45
    CRORE = 1e7

    # =========================
    # Chart 1: CE vs PE OI
    # =========================
    fig1, ax1 = plt.subplots(figsize=(12, 5))

    ax1.bar(x - width / 2, df["CE_OI"] / CRORE, width, color="red", label="CE OI")
    ax1.bar(x + width / 2, df["PE_OI"] / CRORE, width, color="green", label="PE OI")

    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, rotation=90)
    ax1.set_ylabel("Open Interest (Cr)")
    ax1.set_title("CE (Red) vs PE (Green) Open Interest")
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    st.pyplot(fig1)

    # =========================
    # Chart 2: OI Change
    # =========================
    fig2, ax2 = plt.subplots(figsize=(12, 4))

    ax2.bar(x - width / 2, df["CE_OI_CH"] / CRORE, width, color="red", label="CE OI Change")
    ax2.bar(x + width / 2, df["PE_OI_CH"] / CRORE, width, color="green", label="PE OI Change")

    ax2.axhline(0, linewidth=1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(x_labels, rotation=90)
    ax2.set_ylabel("OI Change (Cr)")
    ax2.set_title("Change in OI: CE (Red) vs PE (Green)")
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3)

    st.pyplot(fig2)
    # =========================
    # Chart 3: OI Change
    # =========================
    fig3, ax3 = plt.subplots(figsize=(12, 4))

    ax3.bar(x - width / 2, df["OI_DIFF"] / CRORE, width, color="blue", label="PE-CE OI diff")
    #ax2.bar(x + width / 2, df["PE_OI_CH"] / CRORE, width, color="green", label="PE OI Change")

    ax3.axhline(0, linewidth=1)
    ax3.set_xticks(x)
    ax3.set_xticklabels(x_labels, rotation=90)
    ax3.set_ylabel("OI DIFF (Cr)")
    ax3.set_title("OI differance ")
    ax3.legend()
    ax3.grid(axis="y", alpha=0.3)
    st.pyplot(fig3)
    time.sleep(10)

