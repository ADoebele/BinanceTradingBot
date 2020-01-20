##############################################################################
################## Algorithmic trading (Auto place order) #####################
###############################################################################

import requests
import json
import decimal
import hmac
import time
import pandas as pd
import hashlib




binance_keys = {
    'api_key': "PASTE API KEY HERE",
    'secret_key': "PASTE SECTRET KEY HERE"
}

class Binance:
    def __init__(self):

        self.base = 'https://api.binance.com'

        self.endpoints = {
            "order": '/api/v3/order',
            "testOrder": '/api/v3/order/test',
            "allOrders": '/api/v3/allOrders',
            "klines": '/api/v3/klines',
            "exchangeInfo": '/api/v3/exchangeInfo'
        }

        self.headers = {"X-MBX-APIKEY": binance_keys['api_key']}

    def GetTradingSymbols(self, quoteAssets:list=None):
        #gets all currently tradable symbols
        url = self.base + self.endpoints["exchangeInfo"]

        try:
            response = requests.get(url)
            data = json.loads(response.text)
        except Exception as e:
            print("Exception occured when trying to access "+url)
            print(e)
            return []

        symbols_list = []

        for pair in data['symbols']:
            if pair['status'] == 'TRADING':
                if quoteAssets != None and pair['quoteAsset'] in quoteAssets:  #I would skip BNB here.
                    symbols_list.append(pair['symbol'])

        return(symbols_list)
    
    def GetSymbolData(self, symbol:str, interval:str):

        params = '?&symbol=' + symbol + '&interval='+ interval

        url = self.base + self.endpoints["klines"] + params


        data = requests.get(url)
        dictionary = json.loads(data.text)

        df = pd.DataFrame.from_dict(dictionary)
        df = df.drop(range(6, 12), axis=1)

        col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = col_names

        for col in col_names:
            df[col] = df[col].astype(float)

        df['date'] = pd.to_datetime(df['time'] * 1000000, infer_datetime_format=True)

        return df
