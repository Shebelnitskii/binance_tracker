import os
import pandas as pd
import json
from utils.data_btc import load_data_btc
from utils.data_eth import load_data_eth


def correlation_btc_eth():
    load_data_btc()
    with open('utils/data/data_btc.json', 'r') as file:
        btcusdt_data = json.load(file)

    load_data_eth()
    with open('utils/data/data_eth.json', 'r') as file:
        ethusdt_data = json.load(file)

    data_btc = [{"timestamp": entry["timestamp"], "close_btcusdt": entry["close"]} for entry in
                btcusdt_data]

    data_eth = [{"timestamp": entry["timestamp"], "close_ethusdt": entry["close"]} for entry in ethusdt_data]

    df_btcusdt = pd.DataFrame(data_btc)
    df_ethusdt = pd.DataFrame(data_eth)

    # Объедините данные в один DataFrame по временной метке
    df_merged = pd.merge(df_btcusdt, df_ethusdt, on="timestamp", suffixes=("_btcusdt", "_ethusdt"))

    correlation = df_merged["close_btcusdt"].corr(df_merged["close_ethusdt"])
    print(f"Корреляция между BTCUSDT и ETHUSDT: {correlation}")

    df_merged['datetime'] = pd.to_datetime(df_merged['timestamp'], unit='ms')

    # Установите 'datetime' в качестве индекса
    df_merged.set_index('datetime', inplace=True)

    # Преобразуем столбцы 'close_btcusdt' и 'close_ethusdt' в числа
    df_merged['close_btcusdt'] = pd.to_numeric(df_merged['close_btcusdt'])
    df_merged['close_ethusdt'] = pd.to_numeric(df_merged['close_ethusdt'])

    df_merged['change_btcusdt'] = df_merged['close_btcusdt'].pct_change()
    df_merged['change_ethusdt'] = df_merged['close_ethusdt'].pct_change()

    # Преобразуем данные в проценты, умножив на 100
    df_merged['change_btcusdt'] *= 100
    df_merged['change_ethusdt'] *= 100

    correlation_json = df_merged.to_dict(orient='records')

    # Сохраняем JSON в файл
    with open('utils/data/data_correlation.json', 'w') as json_file:
        json.dump(correlation_json, json_file, indent=4)

    os.remove('utils/data/data_btc.json')
    os.remove('utils/data/data_eth.json')
