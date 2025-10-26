import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def data():
    url = "https://chartink.com/screener/process"

    condition = {"scan_clause" : "( {cash} ( latest rsi( 9 ) > latest wma( latest rsi( 9 ) , 21 ) and 1 day ago  rsi( 9 ) <= 1 day ago  wma( latest rsi( 9 ) , 21 ) and latest rsi( 9 ) > 70 and market cap > 1500 ) ) "}
    condition ={"scan_clause": "( {33489} ( latest close > latest sma( close,100 ) and latest close > latest open and latest close > 1 day ago close * 1.04 and latest volume > 5000000 and [0] 1 hour volume > [=-1] 1 hour volume * 2 and [0] 15 minute wavetrend( 10 , 21 , 4 ) > 30 and [=1] 1 hour close > [=1] 1 hour open ) ) "}
    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]

        header = {"x-csrf-token" : meta}
        data = s.post(url, headers=header, data=condition).json()

        stock_list = pd.DataFrame(data["data"])
        if len(stock_list)==1:
            stk1 =stock_list.iloc[0]['nsecode']
            list=[stk1]
        elif len(stock_list)>=2:
            stk1 = stock_list.iloc[0]['nsecode']
            stk2 =stock_list.iloc[1]['nsecode']
            list=[stk1,stk2]
        elif len(stock_list)==0:
            list=[]

        return list

