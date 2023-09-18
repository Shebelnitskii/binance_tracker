import pandas as pd
import json


def load_correlation():
    with open('utils/data/data_correlation.json', 'r') as file:
        data_correlation = json.load(file)

    data_btc = [{"timestamp": entry["timestamp"], "close_btcusdt": entry["close_btcusdt"]} for entry in
                data_correlation]

    data_eth = [{"timestamp": entry["timestamp"], "close_ethusdt": entry["close_ethusdt"]} for entry in
                data_correlation]

    df_btcusdt = pd.DataFrame(data_btc)
    df_ethusdt = pd.DataFrame(data_eth)

    # Объединяем данные в один DataFrame по временной метке
    df_merged = pd.merge(df_btcusdt, df_ethusdt, on="timestamp", suffixes=("_btcusdt", "_ethusdt"))

    correlation = df_merged["close_btcusdt"].corr(df_merged["close_ethusdt"])

    return correlation
