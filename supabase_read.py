from supabase import create_client
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
IST = ZoneInfo("Asia/Kolkata")

now_ist = datetime.now(IST)
url = "https://cdxnmcpozkfdiqjsthqs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5tY3BvemtmZGlxanN0aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMTk1NzEsImV4cCI6MjA3Nzg5NTU3MX0.wQing-u7lKbYQgXeDvTsTzT5zXVv8Q5Jg1_91PdJxmo"
supabase = create_client(url, key)

def read_token():
    response = supabase.table("token_data").select("*").eq("id", 1).execute()
    data = response.data
    row = data[0]  # first matching row
    token = row["token_details"]
    return token
def get_token():
    response = (
        supabase
        .table("app_token")
        .select("token")
        .eq("id", 1)
        .single()
        .execute()
    )
    return response.data["token"]
def clear():
    response = (
        supabase
        .table("pcr_data")
        .delete()
        .neq("id", 0)  # delete all rows
        .execute()
    )
    return response
def save_pcr_to_supabase(net_ce_oi, net_pe_oi, symbol="NIFTY"):
    # india_timezone = pytz.timezone('Asia/Kolkata')
    # now = datetime.now(india_timezone).time()
    timestamp_ist = datetime.now(IST).replace(second=0, microsecond=0)

    if net_ce_oi == 0:
        return

    pcr = round(net_pe_oi / net_ce_oi, 4)

    # prevent duplicate timestamp insert
    existing = (
        supabase.table("pcr_data")
        .select("id")
        .eq("symbol", symbol)
        .eq("timestamp", timestamp_ist.isoformat())
        .execute()
    )

    if existing.data:
        return

    supabase.table("pcr_data").insert({
        "symbol": symbol,
        "timestamp": timestamp_ist.isoformat(),
        "net_ce_oi": float(net_ce_oi),
        "net_pe_oi": float(net_pe_oi),
        "pcr": pcr
    }).execute()

def fetch_pcr_from_supabase(symbol="NIFTY", limit=120):
    response = (
        supabase.table("pcr_data")
        .select("*")
        .eq("symbol", symbol)
        .order("timestamp", desc=False)
        .limit(limit)
        .execute()
    )

    df = pd.DataFrame(response.data)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Kolkata")
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    df["pcr"] = df["pcr"].astype(float)
    return df
def update_pre_data(ce_oi,pe_oi):
    response = supabase.table("p_data") \
        .update({
        "pre_ce_oi": ce_oi,
        "pre_pe_oi": pe_oi
    }) \
        .eq("id", 1) \
        .execute()

def read_pre_data():
    response = supabase.table("p_data") \
        .select("*") \
        .execute()
    data = response.data[0]
    return data



