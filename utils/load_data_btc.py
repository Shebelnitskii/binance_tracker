from binance import Client
import pandas as pd
import os
import json

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET_KEY")

client = Client(api_key, api_secret)
symbol = 'BTCUSDT'  # Валютная пара, данные которой интересуют
interval = Client.KLINE_INTERVAL_1DAY  # Интервал времени
start_time = "2016-09-01"  # Начальная дата и время в формате 'ГГГГ-ММ-ДД'
end_time = "2023-09-30"  # Конечная дата и время в формате 'ГГГГ-ММ-ДД'

# Получение исторических данных
historical_data = client.get_historical_klines(
    symbol, interval, start_time, end_time)

# Создаём DataFrame из полученных данных
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
           'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(historical_data, columns=columns)

# Преобразуйте столбец timestamp в формат даты и времени
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

df.to_csv('data/data_btc.csv', index=False)

df = pd.read_csv('data/data_btc.csv')

# Преобразуем данные из csv в читабельный json
json_data = []

for index, row in df.iterrows():
    record = {
        "id": index + 1,
        "fields": row.to_dict()  # Данные из строки DataFrame
    }
    json_data.append(record)

with open('data/data_btc.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)
