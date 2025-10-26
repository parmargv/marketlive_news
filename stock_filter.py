import pandas as pd
import pandas_ta as ta
import get_stk_signals
import datetime as dt
import numpy as np
import symbol
from fyers_apiv3 import fyersModel
import os
absolute_path = os.path.dirname(__file__)

def get_data(sym,app_id,token):
    f = dt.date.today() - dt.timedelta(10)
    p = dt.date.today()
    tm = 5
    data = {"symbol": sym, "resolution": tm, "date_format": "1", "range_from": f, "range_to": p, "cont_flag": "1"}
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    nf = fyers.history(data=data)
    return nf
def get_stk_signal(data):
    data = pd.DataFrame(data['candles'], columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
    data['Timestamp'] = (data['Timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
    data['Timestamp'] = data['Timestamp'].dt.tz_localize(None)
    sup = ta.supertrend(data['High'], data['Low'], data['Close'], length=7, multiplier=3.0)
    data = pd.concat([data, sup], axis=1)
    data['sup_s'] = np.where(data['SUPERTd_7_3.0'] == 1, "BUY", "SELL")
    return data
def filter(list,app_id,token):
    n_list=[]
    for ind in list:
        try:
            sym1 = symbol.fut_sym(ind)
            sym = sym1[0]
            df=get_data(sym,app_id,token)
            data=get_stk_signal(df)
            sig = data['sup_s'].iloc[-1]
            sig_t = data['Timestamp'].iloc[-1]

            if sig=="BUY":
                n_list.append(sym)
            else:
                n_list=n_list
        except Exception as e:
            print(f"Error processing {sym}: {e}")
    return n_list

