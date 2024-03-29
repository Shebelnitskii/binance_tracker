from binance import Client
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()


def load_data_eth():
    """
    Функция которая выгружает исторические данные с Binance
    и сохраняет в json файл
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET_KEY")

    client = Client(api_key, api_secret)

    symbol = 'ETHUSDT'  # Валютная пара, данные которой интересуют нас
    interval = Client.KLINE_INTERVAL_12HOUR  # Интервал времени
    start_time = "2023-01-01"  # Начальная дата и время в формате 'ГГГГ-ММ-ДД'
    end_time = "2023-09-30"  # Конечная дата и время в формате 'ГГГГ-ММ-ДД'

    # Получение исторических данных
    historical_data = client.get_historical_klines(symbol, interval, start_time, end_time)

    # Создаём DataFrame из полученных данных
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
               'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

    df = pd.DataFrame(historical_data, columns=columns)

    # Выделяем нужные колонки для сохранения в файл JSON
    selected_columns = ['timestamp', 'close']
    df_selected = df[selected_columns]

    # Преобразуем DataFrame в более плоскую структуру JSON
    data_json = df_selected.to_dict(orient='records')

    # Сохраняем JSON в файл
    with open('utils/data/data_eth.json', 'w') as json_file:
        json.dump(data_json, json_file, indent=4)
