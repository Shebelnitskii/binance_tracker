import pandas as pd
import json


def correlation_btc_eth():
    with open('utils/data/data_btc.json', 'r') as file:
        btcusdt_data = json.load(file)

    with open('utils/data/data_eth.json', 'r') as file:
        ethusdt_data = json.load(file)

    data_btc = [{"timestamp": entry["fields"]["timestamp"], "close_btcusdt": entry["fields"]["close"]} for entry in
                btcusdt_data]

    data_eth = [{"timestamp": entry["fields"]["timestamp"], "close_ethusdt": entry["fields"]["close"]} for entry in
                ethusdt_data]

    df_btcusdt = pd.DataFrame(data_btc)
    df_ethusdt = pd.DataFrame(data_eth)

    # Объедините данные в один DataFrame по временной метке
    df_merged = pd.merge(df_btcusdt, df_ethusdt, on="timestamp", suffixes=("_btcusdt", "_ethusdt"))

    correlation = df_merged["close_btcusdt"].corr(df_merged["close_ethusdt"])
    print(f"Корреляция между BTCUSDT и ETHUSDT: {correlation}")

    df_merged['timestamp'] = pd.to_datetime(df_merged['timestamp'])
    df_merged.set_index('timestamp', inplace=True)

    # Рассчитайте процентное изменение цены ETH
    df_merged['change_btcusdt'] = df_merged['close_btcusdt'].pct_change() * 100
    df_merged['change_ethusdt'] = df_merged['close_ethusdt'].pct_change() * 100

    # Выведите DataFrame
    print(df_merged)
