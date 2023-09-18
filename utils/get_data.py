import requests

def get_btc_price():
    symbol = 'BTCUSDT'
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])


def get_eth_price():
    symbol = 'ETHUSDT'
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])