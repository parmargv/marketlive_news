import requests
import bs4
import pandas as pd
from bs4 import BeautifulSoup as bs
import streamlit as st
import re
def cash():
    url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    r = requests.get(url, {'headers': headers})

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    table3 = soup.find('div', {'class': 'fidi_tbescrol table-responsive'})
    trs = table3.find_all('tr')
    rows = []
    columns = ['DATE', 'FII_BUY', 'FII_SELL', 'FII_NET', 'DII_BUY', 'DII_SELL', 'DII_NET']
    for tr in trs[1:]:
        tds = tr.find_all('td')
        row = [td.text.replace('\n', '').strip() for td in tds]
        rows.append(row)
    df3 = pd.DataFrame(rows, columns=columns)
    df3['DATE'] = df3['DATE'].astype(str)
    df3['DATE'] = df3['DATE'].str[0:11]
    # df3['FII_SELL'] = df3['FII_SELL'].astype('int64')
    # df3 = df3.astype({"FII_SELL": 'str'})
    # df3['FII_SELL']=pd.to_numeric(df3['FII_SELL'],downcast='signed')
    df = df3[2:]

    df = df.copy()

    # --- 1. Prevent accidentally summing an existing TOTAL row (if present) ---
    date_col = df.columns[0]
    df = df[df[date_col] != 'TOTAL'].copy()  # remove any previously appended TOTAL row

    # --- 2. Keep an original-string column for debugging (optional) ---
    if 'FII_NET_raw' not in df.columns:
        df['FII_NET_raw'] = df['FII_NET'].astype(str)

    if 'DII_NET_raw' not in df.columns:
        df['DII_NET_raw'] = df['DII_NET'].astype(str)

    # --- 3. Clean strings: remove commas, spaces; convert (123) -> -123; strip currency symbols etc. ---
    def clean_money(s):
        if pd.isna(s):
            return s
        s = str(s).strip()
        if s == '':
            return None
        # Handle parentheses indicating negative values: (1,234.5) -> -1234.5
        if re.match(r'^\(.*\)$', s):
            s = '-' + s.strip('()')
        # Remove commas and any currency symbols/letters except - and . and digits
        s = re.sub(r'[^\d\.\-]', '', s)
        # There can be multiple dots or multiple minus signs -> leave to numeric coercion
        return s

    df.loc[:, 'FII_NET_clean'] = df['FII_NET_raw'].apply(clean_money)
    df.loc[:, 'DII_NET_clean'] = df['DII_NET_raw'].apply(clean_money)
    # --- 4. Convert to numeric safely ---
    df.loc[:, 'FII_NET'] = pd.to_numeric(df['FII_NET_clean'], errors='coerce')
    df.loc[:, 'DII_NET'] = pd.to_numeric(df['DII_NET_clean'], errors='coerce')
    # --- 5. Report conversion issues so you can inspect what's wrong ---
    bad = df[df['FII_NET'].isna() & df['FII_NET_raw'].notna()]
    if not bad.empty:
        print("Rows that failed numeric conversion (inspect these):")
        print(bad[['FII_NET_raw', 'FII_NET_clean']].head(20))
    else:
        print("All values converted to numeric successfully.")

    # --- 6. Compute the total correctly (ignores NaN) ---

    total_fii = int(df['FII_NET'].sum(skipna=True))
    total_dii = int(df['DII_NET'].sum(skipna=True))
    st.write("TOTAL_FII",total_fii)
    st.write("TOTAL_DII", total_dii)

    # --- 7. (Optional) Append TOTAL row safely: put label in date column only ---
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    # build total row dict: keep same columns order
    df[date_col] = df[date_col].astype(str)
    total_row = {col: None for col in df.columns}
    total_row[date_col] = 'TOTAL'
    for col in numeric_cols:
        total_row[col] = df[col].sum()

    #df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
    # df = df.reset_index()
    # df.sort_index(axis=0,ascending=False)
    return (df)
def cnbc_usa():
    url = "https://www.cnbc.com/world-markets/"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    r = requests.get(url, {'headers': headers})
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h1 = soup.find('div',{'class':'PageBuilder-containerFluidWidths PageBuilder-pageRow'})

    h2 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {'class': 'Card-titleContainer'})[1].find('a').text
    h3 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {'class': 'Card-titleContainer'})[2].find('a').text
    h4 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {'class': 'Card-titleContainer'})[3].find('a').text

    data = {"CNBC_USA": [h1, h2, h3, h4]}
    df = pd.DataFrame(data)
    return df

def cnbc_economy():
    url = "https://www.cnbc.com/economy/"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    r = requests.get(url, {'headers': headers})

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h1 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {
        'class': 'Card-titleContainer'})[0].find('a').text
    h2 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {
        'class': 'Card-titleContainer'})[1].find('a').text
    h3 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {
        'class': 'Card-titleContainer'})[2].find('a').text
    h4 = soup.find('div', {'class': 'PageBuilder-col-9 PageBuilder-col'}).find_all('div', {
        'class': 'Card-titleContainer'})[3].find('a').text

    data = {"CNBC_ECONOMY": [h1, h2, h3, h4]}
    df = pd.DataFrame(data)
    return df
    #.find_all('div', {'class': 'hero-headlines hero-latest-news svelte-13r5oof'}).find_all('div', {'class': 'story-item headlineFz-small svelte-13r5oof'}).find_all('h3').text
def times_now():
    url = "https://economictimes.indiatimes.com/markets"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    r = requests.get(url, {'headers': headers})

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h1 = soup.find('div', {'class': 'FirstFoldWidget_scrollContainer__Ilb4S'})[0].text
    #.find_all('div', {'ul class': 'FirstFoldWidget_timeline___n2Vj'})[0].find('p').text

    # data = {"CNBC_ECONOMY": [h1, h2, h3, h4]}
    # df = pd.DataFrame(data)

#https://www.cnbc.com/economy/
class OI_NIFTY:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def Nifty_gainer(self):
        r = self.session.get(f"https://www.nseindia.com/api/live-analysis-variations?index=gainers",headers=self.headers).json()
        niftyg = [data for data in r['NIFTY']['data']]
        # nifty50_g = [data['PE'] for data in r['filtered']['data'] if "PE" in data]
        df = pd.DataFrame(niftyg)
        return df
    def fo_data(self):
        r = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O",headers=self.headers).json()
        niftyg_fo = [data for data in r['data']]
        # nifty50_g = [data['PE'] for data in r['filtered']['data'] if "PE" in data]
        df = pd.DataFrame(niftyg_fo)
        return df

    def Nifty_looser(self):
        r = self.session.get(f"https://www.nseindia.com/api/live-analysis-variations?index=loosers",headers=self.headers).json()
        niftyl = [data for data in r['NIFTY']['data']]
        # nifty50_g = [data['PE'] for data in r['filtered']['data'] if "PE" in data]
        df = pd.DataFrame(niftyl)
        return df
    def Bn_gainer(self):
        r = self.session.get(f"https://www.nseindia.com/api/live-analysis-variations?index=gainers",headers=self.headers).json()
        Bn_l = [data for data in r['BANKNIFTY']['data']]
        df = pd.DataFrame(Bn_l)
        return df
    def Bn_looser(self):
        r = self.session.get(f"https://www.nseindia.com/api/live-analysis-variations?index=loosers",headers=self.headers).json()
        Bn_l = [data for data in r['BANKNIFTY']['data']]
        df = pd.DataFrame(Bn_l)
        return df

class economics_data():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://tradingeconomics.com/stream", headers=self.headers)

    def News(self):
        r = self.session.get(f"https://tradingeconomics.com/ws/stream.ashx?start=0&size=20",headers=self.headers).json()
        news = [title for title in r]
        df = pd.DataFrame(news)
        return df
class India_news():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://tradingeconomics.com/india/news", headers=self.headers)
    def News_india(self):
        r = self.session.get(f"https://tradingeconomics.com/ws/stream.ashx?start=0&size=20&c=india",headers=self.headers).json()
        news = [title for title in r]
        df = pd.DataFrame(news)
        return df

class fo():
    def gainers(self):
        url = "https://www.moneycontrol.com/stocks/fno/marketstats/futures/gainers/homebody.php?opttopic=gainers&optinst=stkfut&sel_mth=1&sort_order=0"
        headers = {}
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        # req = urllib.request.Request(url, headers=headers)
        # resp = urllib.request.urlopen(req)
        r = requests.get(url, {'headers': headers})
        soup = bs(r.text, 'html.parser')
        table1 = soup.find('div', {'class': 'MT15'})
        trs = table1.find_all('tr')
        rows = []
        columns = ['SYMB', 'EXP', 'LTP', 'CH', 'CH(%)', 'H-L', 'AVG', 'VOL', 'VALUE', 'OI', 'OI-CH']
        for tr in trs[1:]:
            tds = tr.find_all('td')
            row = [td.text.replace('\n', '').strip() for td in tds]
            rows.append(row)
        df1 = pd.DataFrame(rows, columns=columns)
        df1.drop(['VALUE'], axis=1, inplace=True)
        df1.reset_index(drop=True, inplace=False)

        oi = df1['OI-CH'].str.split("\r", expand=True)

        vol = df1['VOL'].str.split("\r\t\t\t\t\t\t\t\t", expand=True)
        df1.drop(['EXP', 'CH', 'H-L', 'AVG', 'OI-CH', 'VOL'], axis=1, inplace=True)
        df1["OI"] = oi[0]
        df1["OI(%)"] = oi[1]
        df1.drop(['OI'], axis=1, inplace=True)
        df1["VOL"] = vol[0]
        df11 = df1.iloc[0:10, 0:4]
        return df11
    def loosers(self):
        url = "https://www.moneycontrol.com/stocks/fno/marketstats/futures/losers/homebody.php?opttopic=losers&optinst=stkfut&sel_mth=1&sort_order=0"
        headers = {}
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        # req = urllib.request.Request(url, headers=headers)
        # resp = urllib.request.urlopen(req)
        r = requests.get(url, {'headers': headers})
        soup = bs(r.text, 'html.parser')
        table2 = soup.find('div', {'class': 'MT15'})
        trs = table2.find_all('tr')
        rows = []
        columns = ['SYMB', 'EXP', 'LTP', 'CH', 'CH(%)', 'H-L', 'AVG', 'VOL', 'VALUE', 'OI', 'OI-CH']
        for tr in trs[1:]:
            tds = tr.find_all('td')
            row = [td.text.replace('\n', '').strip() for td in tds]
            rows.append(row)
        df2 = pd.DataFrame(rows, columns=columns)

        df2.drop(['VALUE'], axis=1, inplace=True)
        df2.reset_index(drop=True, inplace=False)
        oi = df2['OI-CH'].str.split("\r", expand=True)
        vol = df2['VOL'].str.split("\r\t\t\t\t\t\t\t\t", expand=True)
        df2.drop(['EXP', 'CH', 'H-L', 'AVG', 'OI-CH', 'VOL'], axis=1, inplace=True)
        df2["OI"] = oi[0]
        df2["OI(%)"] = oi[1]
        df2.drop(['OI'], axis=1, inplace=True)
        # df2["VOL"] = vol[0]
        df22 = df2.iloc[0:10, 0:4]
        return df22
class money():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://www.moneycontrol.com/markets/global-indices/", headers=self.headers)

    def us_market(self):
        r = self.session.get(f"https://priceapi.moneycontrol.com/technicalCompanyData/globalMarket/getGlobalIndicesListingData?view=overview&deviceType=W",
                             headers=self.headers).json()
        us_market_data = next(item['data'] for item in r['dataList'] if item['heading'] == 'US_Market')
        columns = [item['name'] for item in r['header']]
        us_market_df = pd.DataFrame(us_market_data, columns=columns)
        selected_columns = ['name', 'price', 'net_change', 'percent_change']
        us_market_selected_df = us_market_df[selected_columns]
        return us_market_selected_df
    def euro_market(self):
        r = self.session.get(f"https://priceapi.moneycontrol.com/technicalCompanyData/globalMarket/getGlobalIndicesListingData?view=overview&deviceType=W",
                             headers=self.headers).json()
        euro_market_data = next(item['data'] for item in r['dataList'] if item['heading'] == 'European_Market')
        columns = [item['name'] for item in r['header']]
        us_market_df = pd.DataFrame(euro_market_data, columns=columns)
        selected_columns = ['name', 'price', 'net_change', 'percent_change']
        us_market_selected_df = us_market_df[selected_columns]
        return us_market_selected_df
    def asia_market(self):
        r = self.session.get(f"https://priceapi.moneycontrol.com/technicalCompanyData/globalMarket/getGlobalIndicesListingData?view=overview&deviceType=W",
                             headers=self.headers).json()
        asia_market_data = next(item['data'] for item in r['dataList'] if item['heading'] == 'Asian_Market')

        columns = [item['name'] for item in r['header']]
        us_market_df = pd.DataFrame(asia_market_data, columns=columns)
        selected_columns = ['name', 'price', 'net_change', 'percent_change']
        us_market_selected_df = us_market_df[selected_columns]
        return us_market_selected_df
class groww():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://groww.in/indices/global-indices", headers=self.headers)
    def Gobal_Indices(self):
        r = self.session.get(f"https://groww.in/v1/api/stocks_data/v1/global_instruments?instrumentType=GLOBAL_INSTRUMENTS",headers=self.headers).json()
        indices = [data for data in r['aggregatedGlobalInstrumentDto']]
        # nifty50_g = [data['PE'] for data in r['filtered']['data'] if "PE" in data]
        df = pd.DataFrame(indices)
        return df
def groww_data():
    d=groww()
    data=d.Gobal_Indices()
    giftnifty = data['livePriceDto']
    gnifty = (data['livePriceDto'][0])
    gift_ltp = int(gnifty['value'])
    gift_ch = int(gnifty['dayChange'])
    gift_per = (gnifty['dayChangePerc'])
    dow_f = (data['livePriceDto'][1])
    dowf_ltp = int(dow_f['value'])
    dowf_ch = int(dow_f['dayChange'])
    dowf_per = (dow_f['dayChangePerc'])
    dow = (data['livePriceDto'][3])
    dow_ltp = int(dow['value'])
    dow_ch = int(dow['dayChange'])
    dow_per = (dow['dayChangePerc'])
    nas = (data['livePriceDto'][2])
    nas_ltp = int(nas['value'])
    nas_ch = int(nas['dayChange'])
    nas_per = (nas['dayChangePerc'])
    sp=(data['livePriceDto'][4])
    sp_ltp = int(sp['value'])
    sp_ch = int(sp['dayChange'])
    sp_per = (sp['dayChangePerc'])
    nk=(data['livePriceDto'][5])
    nk_ltp = int(nk['value'])
    nk_ch = int(nk['dayChange'])
    nk_per = (nk['dayChangePerc'])
    hs=(data['livePriceDto'][6])
    hs_ltp = int(hs['value'])
    hs_ch = int(hs['dayChange'])
    hs_per = (hs['dayChangePerc'])
    dax=(data['livePriceDto'][7])
    dax_ltp = int(dax['value'])
    dax_ch = int(dax['dayChange'])
    dax_per = (dax['dayChangePerc'])
    ftse=(data['livePriceDto'][8])
    ftse_ltp = int(ftse['value'])
    ftse_ch = int(ftse['dayChange'])
    ftse_per = (ftse['dayChangePerc'])
    cac=(data['livePriceDto'][7])
    cac_ltp = int(cac['value'])
    cac_ch = int(cac['dayChange'])
    cac_per = (cac['dayChangePerc'])
    data = {
        "INDICES":['GIFT_NIFTY','DOW_FUT','DOW','NASDAQ','S&P','NIKKIE','HANG_SANG','DAX','FTSE','CAC'],
        "%":[gift_per,dowf_per,dow_per,nas_per,sp_per,nk_per,hs_per,dax_per,ftse_per,cac_per],
        "CHAGE":[gift_ch,dowf_ch,dow_ch,nas_ch,sp_ch,nk_ch,hs_ch,dax_ch,ftse_ch,cac_ch],
        "LTP":[gift_ltp,dowf_ltp,dow_ltp,nas_ltp,sp_ltp,nk_ltp,hs_ltp,dax_ltp,ftse_ltp,cac_ltp]
    }

    df = pd.DataFrame(data)
    return df
def gainer_looser_fo():
    col1, col2 = st.columns(2)
    with col1:
        nifty = OI_NIFTY()
        FO = nifty.fo_data()
        data = (FO)
        df = data[['symbol', 'pChange']]
        gainer_df = df.sort_values(by='pChange', ascending=False)

        df11 = gainer_df.head(10)

        st.markdown(f'<h1 style="color:#3f8c92;font-size:15px;">{"Top 10 F&O Gainers"}</h1>',unsafe_allow_html=True)
        # st.markdown(f'<marquee behavior="scroll" direction="left">Here is some scrolling text... right to left!</marquee>', unsafe_allow_html=True)
        hide_table_row_index = """
                                                                                                                                                                                           <style>
                                                                                                                                                                                           tbody th {display:none}
                                                                                                                                                                                           .blank {display:none}
                                                                                                                                                                                           </style>
                                                                                                                                                                                           """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        st.table(df11.style.set_table_styles([{'selector': 'table', 'props': [('max-width', '100%')]}]))
        # st.table(gainer_df)
    with col2:
        nifty = OI_NIFTY()
        FO = nifty.fo_data()
        data = (FO)
        df = data[['symbol', 'pChange']]
        looser_df = df.sort_values(by='pChange', ascending=True)

        df22 = looser_df.head(10)

        # df22.set_index('OI(%)',inplace=False)
        st.markdown(f'<h1 style="color:#E11F2A;font-size:15px;">{"Top 10 F&O Losers"}</h1>', unsafe_allow_html=True)
        hide_table_row_index = """
                                                                                                                                                                               <style>
                                                                                                                                                                               tbody th {display:none}
                                                                                                                                                                               .blank {display:none}
                                                                                                                                                                               </style>
                                                                                                                                                                               """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        st.table(df22.style.set_table_styles([{'selector': 'table', 'props': [('max-width', '100%')]}]))
        #st.table(looser_df)

def gainer_looser_nf():
    col1, col2 = st.columns(2)
    with col1:
        nifty = OI_NIFTY()
        df1 = nifty.Nifty_gainer()
        print(df1)
        df11 = df1[['symbol', 'perChange']]
        df21 = df11.head(10)
        # df11 = df1.iloc[0:9, [0, 5, 6, 7]]
        # df2 = nifty.Nifty_looser()
        # df22 = df2.iloc[0:9, [0, 5, 6, 7]]
        # df22 = df2[df2.columns[cols]]
        st.markdown(f'<h1 style="color:#3f8c92;font-size:15px;">{"Nifty Gainers"}</h1>', unsafe_allow_html=True)
        # st.markdown(f'<marquee behavior="scroll" direction="left">Here is some scrolling text... right to left!</marquee>', unsafe_allow_html=True)
        hide_table_row_index = """
                                                                                                                                                                                           <style>
                                                                                                                                                                                           tbody th {display:none}
                                                                                                                                                                                           .blank {display:none}
                                                                                                                                                                                           </style>
                                                                                                                                                                                           """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # df33 = df_g.iloc[0:1, 0:4]
        st.table(df21.style.set_table_styles([{'selector': 'table', 'props': [('max-width', '100%')]}]))
    with col2:
        nifty = OI_NIFTY()
        df1 = nifty.Nifty_looser()
        df12 = df1[['symbol', 'perChange']]
        df22 = df12.head(10)
        st.markdown(f'<h1 style="color:#E11F2A;font-size:15px;">{"Nifty Loosers"}</h1>', unsafe_allow_html=True)
        # st.markdown(f'<marquee behavior="scroll" direction="left">Here is some scrolling text... right to left!</marquee>', unsafe_allow_html=True)
        hide_table_row_index = """
                                                                                                                                                                                                       <style>
                                                                                                                                                                                                       tbody th {display:none}
                                                                                                                                                                                                       .blank {display:none}
                                                                                                                                                                                                       </style>
                                                                                                                                                                                                       """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # df44 = df_l.iloc[0:1, 0:4]
        st.table(df22.style.set_table_styles([{'selector': 'table', 'props': [('max-width', '100%')]}]))

# nifty =OI_NIFTY()
# FO =nifty.Nifty_gainer()
# df1 = FO[['symbol', 'perChange']]
# print(df1)



#
# gainer_df = df.sort_values(by='pChange',ascending=False)
#
# looser_df = df.sort_values(by='pChange',ascending=True)
# print(gainer_df.head(10))
# print(looser_df.head(10))
#print(data.iloc[0])
#print(data.iloc[0]['symbol'])
# print(data.iloc[0]['pChange'])
# stk_name =data['symbole']
# stk_name =data['symbole']
