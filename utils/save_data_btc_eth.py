import os
import pandas as pd
import json
from utils.data_btc import load_data_btc
from utils.data_eth import load_data_eth


def save_changes_eth_btc():
    """
    Функция которая считывает данные по ETH и BTC производит карреляцию, объеденение и подсчёт процентного
    изменения валюты, сохраняя в отдельный json файл
    """
    # Проверяем наличие файла historical_data.json
    if os.path.exists('utils/data/historical_data.json'):
        print("-" * 35)
        print("Данные по историческим данным уже существуют. Функция не будет выполнена.")
        print("-" * 35)
        return
    else:
        print("-" * 35)
        print("Исторические данные не найдены! Идёт создание нового файла historical_data.json")
        print("-" * 35)

    # Вызываем функцию load_data_btc для загрузки исторических данных в json файл
    load_data_btc()
    with open('utils/data/data_btc.json', 'r') as file:
        btcusdt_data = json.load(file)

    # Вызываем функцию load_data_eth для загрузки исторических данных в json файл
    load_data_eth()
    with open('utils/data/data_eth.json', 'r') as file:
        ethusdt_data = json.load(file)

    data_btc = [{"timestamp": entry["timestamp"], "close_btcusdt": entry["close"]} for entry in
                btcusdt_data]

    data_eth = [{"timestamp": entry["timestamp"], "close_ethusdt": entry["close"]} for entry in ethusdt_data]

    df_btcusdt = pd.DataFrame(data_btc)
    df_ethusdt = pd.DataFrame(data_eth)

    # Объединяем данные в один DataFrame по временной метке
    df_merged = pd.merge(df_btcusdt, df_ethusdt, on="timestamp", suffixes=("_btcusdt", "_ethusdt"))

    df_merged['datetime'] = pd.to_datetime(df_merged['timestamp'], unit='ms')

    # Установливаем datetime в качестве индекса
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
    with open('utils/data/historical_data.json', 'w') as json_file:
        json.dump(correlation_json, json_file, indent=4)

    # Удаляем ненужные файлы
    os.remove('utils/data/data_btc.json')
    os.remove('utils/data/data_eth.json')
