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
    token = supabase_read.get_token()
    return token


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
    token = get_token()
    data = fetch_oi(token, "NSE:NIFTY50-INDEX")

    df = data[0]
    c_oi = data[1]
    p_oi = data[2]
    s1 = data[3]
    s2 = data[4]
    r1 = data[5]
    r2 = data[6]
    CRORE = 1e7
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.write("R1", r1)
    with col2:
        st.write("R2", r2)
    with col3:
        st.write("S1", s1)
    with col4:
        st.write("S2", s2)


    # ------------------ FIGURE ------------------
    fig, (ax1, ax2) = plt.subplots(
        1, 2,
        figsize=(12, 4),
        gridspec_kw={'width_ratios': [3, 1]}  # left wide, right compact
    )

    # =====================================================================
    # CHART 1 (LEFT): STRIKE-WISE OI
    # =====================================================================
    x_labels = df["strike_price"].astype(str)
    x = np.arange(len(x_labels))
    width = 0.45

    ax1.bar(x - width / 2, df["CE_OI"] / CRORE, width, color="red", label="CE OI")
    ax1.bar(x + width / 2, df["PE_OI"] / CRORE, width, color="green", label="PE OI")

    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, rotation=90)
    ax1.set_ylabel("Open Interest (Cr)")
    ax1.set_title("Strike-wise OI")
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    # =====================================================================
    # CHART 2 (RIGHT): NET CE vs NET PE OI
    # =====================================================================
    labels = ["Net CE OI", "Net PE OI"]
    values = [c_oi/CRORE, p_oi/CRORE]

    x2 = np.arange(len(labels))
    bar_width = 0.4

    ax2.bar(x2[0], values[0], bar_width, color="red", label="Net CE OI")
    ax2.bar(x2[1], values[1], bar_width, color="green", label="Net PE OI")

    y_max = max(values) * 1.2
    ax2.set_ylim(0, y_max)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel("OI (Cr)")
    ax2.set_title("Net OI", fontsize=10)
    ax2.grid(axis="y", alpha=0.3)

    # Value labels
    for i, v in enumerate(values):
        ax2.text(i, v + y_max * 0.02, f"{v:.2f}", ha="center", fontsize=9)

    # ------------------ FINAL ------------------
    plt.tight_layout()
    st.pyplot(fig)
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

def plot_pcr():
    token = supabase_read.get_token()
    data = fetch_oi(token, "NSE:NIFTY50-INDEX")
    df = data[0]
    c_oi = data[1]
    p_oi = data[2]

    if "pcr_df" not in st.session_state:
        st.session_state.pcr_df = pd.DataFrame(
            columns=["timestamp", "net_ce_oi", "net_pe_oi", "pcr"]
        )

    def store_pcr(net_ce_oi, net_pe_oi):
        timestamp = datetime.now().replace(second=0, microsecond=0)

        pcr = net_pe_oi / net_ce_oi if net_ce_oi != 0 else np.nan

        new_row = {
            "timestamp": timestamp,
            "net_ce_oi": net_ce_oi,
            "net_pe_oi": net_pe_oi,
            "pcr": pcr
        }

        st.session_state.pcr_df = pd.concat(
            [st.session_state.pcr_df, pd.DataFrame([new_row])],
            ignore_index=True
        )

    store_pcr(c_oi, p_oi)

    st.session_state.pcr_df["pcr_sma_10"] = (
        st.session_state.pcr_df["pcr"]
        .rolling(window=10, min_periods=1)
        .mean()
    )

    df_plot = st.session_state.pcr_df

    fig, ax = plt.subplots(figsize=(10, 4))

    # PCR line
    ax.plot(
        df_plot["timestamp"],
        df_plot["pcr"],
        linewidth=2,
        label="PCR"
    )

    # SMA(10) line
    ax.plot(
        df_plot["timestamp"],
        df_plot["pcr_sma_10"],
        linestyle="--",
        linewidth=2,
        label="PCR SMA(10)"
    )

    # Reference line
    ax.axhline(1, linestyle=":", alpha=0.6)

    ax.set_title("PCR vs Time (1-Min) with SMA(10)")
    ax.set_xlabel("Time")
    ax.set_ylabel("PCR")

    ax.grid(alpha=0.3)
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)