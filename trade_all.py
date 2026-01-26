import pandas as pd
from fyers_apiv3 import fyersModel
import os
import toml

def load_users(toml_file):
    with open('user_data.toml', 'r') as file:
        return toml.load(file)

users = load_users('users.toml')

def authenticate_user(users):
    for user, details in users.items():
        user_name = details['account']
        application_id = details['app_id']

        return user_name, application_id


data = authenticate_user(users)
u_name = data[0]
app_id = data[1]
absolute_path = os.path.dirname(__file__)

def quate(token,sym):
    data = {"symbols":sym}
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    response = fyers.quotes(data=data)
    data = response['d'][0]['v']
    ch_per = data['chp']
    last_price = data['lp']
    prev_close = data['prev_close_price']
    open_price = data['open_price']
    ch = round(last_price - prev_close,2)
    return last_price,ch,ch_per,open_price

def live_data(token,symbol):
    data = {"symbols": symbol}
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    response = fyers.quotes(data=data)
    data1 = response
    data =data1['d']
    df = pd.DataFrame(data)
    d_nf =df['v'][0]
    p_c = d_nf['prev_close_price']
    ltp = d_nf['lp']
    open = d_nf['open_price']
    ch_p = d_nf['chp']
    high = d_nf['high_price']
    low = d_nf['low_price']
    ch =int(ltp - p_c)
    open_gap =round(((open - p_c)/p_c)*100,2)
    return open_gap,ch_p,ch,high,ltp,low,p_c

def o_chain(token,sym,o_price):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, is_async=False, log_path=absolute_path)
    data = {
        "symbol": sym,
        "strikecount": 10,
        "timestamp": ""
    }
    res = fyers.optionchain(data=data);
    c_oi = res['data']['callOi']
    p_oi = res['data']['putOi']
    data = res['data']['optionsChain']
    strike_data = {}

    for option in data:
        strike = option.get('strike_price')
        if strike == -1:  # skip the non-option data
            continue

        if strike not in strike_data:
            strike_data[strike] = {
                'strike_price': strike,
                'CE_OI': None,
                'CE_OI_CH': None,
                'PE_OI': None,
                'PE_OI_CH': None,
                'OI_DIFF': None
            }

        if option['option_type'] == 'CE':
            strike_data[strike]['CE_OI'] = option.get('oi')
            strike_data[strike]['CE_OI_CH'] = option.get('oich')

        elif option['option_type'] == 'PE':
            strike_data[strike]['PE_OI'] = option.get('oi')
            strike_data[strike]['PE_OI_CH'] = option.get('oich')

    # Convert to DataFrame
    df = pd.DataFrame(strike_data.values())

    df['OI_DIFF'] = df['PE_OI'] - df['CE_OI']
    df['OI_CH_DIFF']=df['PE_OI_CH']-df['CE_OI_CH']

    # ce_oi = df['CE_OI'].sum()
    # pe_oi = df['PE_OI'].sum()


    df = df.sort_values('strike_price').reset_index(drop=True)
    df_h = df[df['strike_price'] >= o_price]
    df_1 = df_h.head(9)
    df_l = df[df['strike_price'] < o_price]
    df_2 = df_l.tail(7)
    df = pd.concat([df_1, df_2], axis=0)
    df = df.sort_values('strike_price').reset_index(drop=True)
    ce_oi = df['CE_OI'].sum()
    pe_oi = df['PE_OI'].sum()
    ce_oi_ch = df['CE_OI_CH'].sum()
    pe_oi_ch = df['PE_OI_CH'].sum()
    df = df.sort_values('CE_OI').reset_index(drop=True)
    df = df.sort_values('strike_price').reset_index(drop=True)
    pcr = p_oi / c_oi
    return df,c_oi,p_oi,pcr,ce_oi_ch,pe_oi_ch,ce_oi,pe_oi
def buy_order(token, sym, qnt, buyat):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {
        "symbol": sym,
        "qty": qnt,
        "type": 1,
        "side": 1,
        "productType": "MARGIN",
        "limitPrice": buyat,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        # "stopLoss":sl,
        # "takeProfit":trg,

    }
    response = fyers.place_order(data=data)
    st = response.get("s")
    code = response.get("code")
    message = response.get("message")
    id = str(response.get("id"))
    return code, message, id, st

def buy_order_m(token, sym, qnt):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {
        "symbol": sym,
        "qty": qnt,
        "type": 2,
        "side": 1,
        "productType": "MARGIN",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        # "stopLoss":sl,
        # "takeProfit":trg,

    }
    response = fyers.place_order(data=data)
    st = response.get("s")
    code = response.get("code")
    message = response.get("message")
    id = str(response.get("id"))
    return code, message, id, st

def sell_order(token, sym, qnt, sellat):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {
        "symbol": sym,
        "qty": qnt,
        "type": 1,
        "side": -1,
        "productType": "MARGIN",
        "limitPrice": sellat,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        # "stopLoss":sl,
        # "takeProfit":trg,

    }
    response = fyers.place_order(data=data)
    st = response.get("s")
    code = response.get("code")
    message = response.get("message")
    id = str(response.get("id"))
    return code, message, id, st

def basket_order(token, sym1, sym2, qnt):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = [{
        "symbol": sym1,
        "qty": qnt,
        "type": 2,
        "side": -1,
        "productType": "MARGIN",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        # "stopLoss":sl,
        # "takeProfit":trg,

    },
        {
            "symbol": sym2,
            "qty": qnt,
            "type": 2,
            "side": 1,
            "productType": "MARGIN",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            # "stopLoss":sl,
            # "takeProfit":trg,

        }
    ]
    response = fyers.place_basket_orders(data=data)
    return response

def exit_one(token, id):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {"id": id}
    response = fyers.exit_positions(data=data)
    st = response.get("s")
    code = response.get("code")
    message = response.get("message")
    id = str(response.get("id"))
    return code, message, id, st

def exit_two(token, id1, id2):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = [
        {"id": id1},
        {"id": id2}
    ]
    response = fyers.exit_positions(data=data)
    return response


def exit_all(token):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {}
    response = fyers.exit_positions(data=data)
    return response


# def tb(token):
#     session = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
#     res = session.tradebook() # Fetch the tradebook data
#     trade_books = res.get("tradeBook", [])
#
#     # Check if the tradebook is empty
#     if not trade_books:
#         return pd.DataFrame()  # Return an empty DataFrame
#
#     # Collect all trades data
#     all_trades_data = []
#     for trade in trade_books:
#         trade_data = {
#             "clientId": trade.get("clientId"),
#             "orderDateTime": trade.get("orderDateTime"),
#             "orderNumber": trade.get("orderNumber"),
#             "exchangeOrderNo": trade.get("exchangeOrderNo"),
#             "exchange": trade.get("exchange"),
#             "side": trade.get("side"),
#             "segment": trade.get("segment"),
#             "orderType": trade.get("orderType"),
#             "fyToken": trade.get("fyToken"),
#             "productType": trade.get("productType"),
#             "tradedQty": trade.get("tradedQty"),
#             "tradePrice": trade.get("tradePrice"),
#             "tradeValue": trade.get("tradeValue"),
#             "tradeNumber": trade.get("tradeNumber"),
#             "row": trade.get("row"),
#             "symbol": trade.get("symbol"),
#         }
#         all_trades_data.append(trade_data)  # Correctly append to the list
#
#     # Convert list of trades to DataFrame
#     df = pd.DataFrame(all_trades_data)
#     print(df)
#
#     return df
def tb(token):
    session = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    res = session.tradebook() # Fetch the tradebook data
    trade_books = res.get("tradeBook", [])
    # Check if the tradebook is empty
    if not trade_books:
        return pd.DataFrame()  # Return an empty DataFrame

    # Collect all trades data
    all_trades_data = []
    for trade in trade_books:
        trade_data = {
            "orderDateTime": trade.get("orderDateTime"),
            "side": trade.get("side"),
            "orderType": trade.get("orderType"),
            "tradedQty": trade.get("tradedQty"),
            "tradePrice": trade.get("tradePrice"),
            "symbol": trade.get("symbol"),
        }
        all_trades_data.append(trade_data)  # Correctly append to the list

    # Convert list of trades to DataFrame
    df = pd.DataFrame(all_trades_data)
    df['orderDateTime'] = pd.to_datetime(df['orderDateTime'], format="%d-%b-%Y %H:%M:%S")
    df = df.sort_values(by='orderDateTime', ascending=False)
    df = df.reset_index(drop=True)
    return df

def tb_data(token,symbol):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    res = fyers.tradebook()
    if res["s"] == "ok":
        trade_data = res["tradeBook"]
        # target_symbols = ["NSE:NIFTY", "NSE:BANKNIFTY"]
        filtered_trades = [trade for trade in trade_data if any(symbol in trade["symbol"] for symbol in symbol)]
        return filtered_trades
    else:
        print("Failed to fetch trade data:", res["message"])

def np(token):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    res = fyers.positions()
    data = res
    overall_count_total = data["overall"]["count_total"]
    overall_count_open = data["overall"]["count_open"]
    overall_pl_total = data["overall"]["pl_total"]
    overall_pl_realized = data["overall"]["pl_realized"]
    overall_pl_unrealized = data["overall"]["pl_unrealized"]

    count = overall_count_total
    data_list = []
    for i in range(count):
        symbol = data["netPositions"][i]["symbol"]
        buy_qty = data["netPositions"][i]["buyQty"]
        buy_avg = data["netPositions"][i]["buyAvg"]
        sell_qty = data["netPositions"][i]["sellQty"]
        sell_avg = data["netPositions"][i]["sellAvg"]
        net_qnt = data["netPositions"][i]["netQty"]
        net_pro = data["netPositions"][i]["realized_profit"]
        cur_pro = data["netPositions"][i]["unrealized_profit"]
        row_data = [symbol, buy_qty, buy_avg, sell_qty, sell_avg, net_qnt, net_pro,cur_pro]
        data_list.append(row_data)

    data_df = pd.DataFrame(data_list,
                           columns=["Symbol", "BuyQty", "BuyAvg", "SellQty", "SellAvg", "Net_qnt", "Net_profit","Cur_profit"])
    return data_df, overall_count_total, overall_count_open, overall_pl_total, overall_pl_realized, overall_pl_unrealized


def ob(token):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    res = fyers.orderbook()
    # or_book = res.get("orderBook")
    # df = pd.DataFrame(or_book)
    #order_message = res['orderBook'][0]['message']
    status_mapping = {
        1: 'Canceled',
        2: 'Traded / Filled',
        3: '(Not used currently)',
        4: 'Transit',
        5: 'Rejected',
        6: 'Pending',
        7: 'Expired'
    }
    order_data = [
        {
            "symbol": order.get("symbol", ""),
            "status": order.get("status", ""),
            "filledQty":order.get("filledQty", ""),
            "remainingQuantity": order.get("remainingQuantity", 0),
            "tradedPrice": order.get("tradedPrice", 0.0),
            "message": order.get("message", "")
        }
        for order in res.get("orderBook", [])
    ]

    # Create DataFrame
    df = pd.DataFrame(order_data)
    if len(df) != 0:
        df['status_description'] = df['status'].map(status_mapping)
        df = df[['symbol','status_description',"filledQty", 'remainingQuantity', 'tradedPrice', 'message']]
    else:
        df =[]
    # messages = [order.get('message', '') for order in res.get('orderBook', [])]
    return df


def ob_one(token, id):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {"id": id}
    res = fyers.orderbook(data)
    or_book = res.get("orderBook")
    if len(or_book) == 0:
        status = 0
    else:
        status = or_book['status']
    return status


def depth_data(token, symbol):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    data = {
        "symbol": symbol,
        "ohlcv_flag": "1"
    }
    response = fyers.depth(data=data)
    data1 = response.get('d')
    data2 = data1.get('NSE:NIFTY24NOV23300CE')
    buy_qnt = data2.get("totalbuyqty")
    sell_qnt = data2.get("totalsellqty")
    oi = data2.get("oi")
    p_oi = data2.get("pdoi")
    oi_ch = data2.get("oipercent")
    ltp = data2.get("ltp")
    return buy_qnt,sell_qnt,p_oi,oi,oi_ch,ltp


def fund(token):
    fyers = fyersModel.FyersModel(client_id=app_id, token=token, log_path=absolute_path)
    response = fyers.funds()
    fund_limit = response.get("fund_limit")
    data1 = fund_limit[0]
    t_b = fund_limit[0].get("equityAmount")
    u_a = fund_limit[1].get("equityAmount")
    c_b = fund_limit[2].get("equityAmount")
    r_p_l = fund_limit[3].get("equityAmount")

    return t_b, u_a, c_b, r_p_l
