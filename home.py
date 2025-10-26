import bs4
import urllib
from urllib.request import Request, urlopen
import requests
import pandas as pd


def economics():
    url = 'https://economictimes.indiatimes.com/markets/stocks/news'
    # url = 'https://www.business-standard.com/category/markets-news-1060101.htm'
    headers = {
        'user-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

    }

    r = requests.get(url, {'headers': headers})

    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    h1 = soup.find_all('div', {'class': 'eachStory'})[0].find_all('h3')[0].text

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h2 = soup.find_all('div', {'class': 'eachStory'})[1].find_all('h3')[0].text

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h3 = soup.find_all('div', {'class': 'eachStory'})[2].find_all('h3')[0].text

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h4 = soup.find_all('div', {'class': 'eachStory'})[3].find_all('h3')[0].text
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    h5 = soup.find_all('div', {'class': 'eachStory'})[4].find_all('h3')[0].text

    data = {"Economics Times":[h1, h2, h3, h4]}
    df = pd.DataFrame(data)
    return df


def earning():
    url = 'https://economictimes.indiatimes.com/markets/stocks/earnings'

    headers = {
        'user-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

    }

    r = requests.get(url, {'headers': headers})
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    i = len(soup.find_all('div', {'class': 'subSec'})[0].find_all('a'))

    h23 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[1].text
    h24 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[3].text
    h25 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[5].text
    h26 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[7].text
    h27 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[9].text
    h28 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[11].text
    h29 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[13].text
    h30 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[15].text
    h31 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[17].text
    h32 = soup.find_all('div', {'class': 'subSec'})[0].find_all('a')[19].text
    data = {'Economics times Earning news': [h23, h24, h25, h26, h27]}
    df = pd.DataFrame(data)
    return df
def bloomberg():
    url = "https://www.bloombergquint.com/"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    r = requests.get(url, {'headers': headers})

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    hc = len(soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a'))
    h33 = soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a')[1].text
    h34 = soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a')[2].text
    h35 = soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a')[3].text
    h36 = soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a')[4].text
    h37 = soup.find_all('div', {'class': 'latest-updates-m__latest-updates__QOCdR'})[0].find_all('a')[5].text
    data4 = {"Bloomberg":[h33, h34, h35, h36, h37]}
    df = pd.DataFrame(data4)
    return df

def cnbc():
    url = "https://www.cnbctv18.com/market/stocks/"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)

    soup = bs4.BeautifulSoup(resp, 'html.parser')
    h33 = soup.find_all('div', {'class': 'jsx-95506e352219bddb story-meta'})[0].find_all('h2',{'class':'jsx-95506e352219bddb story-title'})[0].text
    h34 = soup.find_all('div', {'class': 'jsx-95506e352219bddb story-meta'})[1].find_all('h2', {'class': 'jsx-95506e352219bddb story-title'})[0].text
    h35 = soup.find_all('div', {'class': 'jsx-95506e352219bddb story-meta'})[2].find_all('h2', {'class': 'jsx-95506e352219bddb story-title'})[0].text
    h36 = soup.find_all('div', {'class': 'jsx-95506e352219bddb story-meta'})[3].find_all('h2', {'class': 'jsx-95506e352219bddb story-title'})[0].text
    #data3 = {'CNBC News': [h33, h34, h35, h36]}
    data33 = {"CNBC News":[h33, h34,h35,h36]}
    df = pd.DataFrame(data33)
    return df
def bt():
    url = "https://www.businesstoday.in/markets/company-stock"
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(resp, 'html.parser')
    h11 = soup.find_all('div', {'class': 'widget-listing'})[0].text
    h22 = soup.find_all('div', {'class': 'widget-listing'})[1].text
    h33 = soup.find_all('div', {'class': 'widget-listing'})[2].text
    h44 = soup.find_all('div', {'class': 'widget-listing'})[3].text
    h55 = soup.find_all('div', {'class': 'widget-listing'})[4].text
    words = h11.split()
    h11 = ' '.join(words[:15])
    words = h22.split()
    h22 = ' '.join(words[:15])
    words = h33.split()
    h33 = ' '.join(words[:15])
    words = h44.split()
    h44 = ' '.join(words[:15])
    words = h55.split()
    h55 = ' '.join(words[:15])
    list={'Bussiness today':[h11,h22,h33,h44,h55]}
    df = pd.DataFrame(list)
    return df

