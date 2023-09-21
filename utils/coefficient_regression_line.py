import json
import pandas as pd
import statsmodels.api as sm


def load_coefficient_btc():
    # Загрузка данных из JSON-файла
    with open('utils/data/historical_data.json', 'r') as json_file:
        data = json.load(json_file)

    # Создание DataFrame на основе данных из JSON
    df = pd.DataFrame(data)

    # Определение независимой переменной (BTC) и зависимой переменной (ETH)
    X = df['close_btcusdt']
    Y = df['close_ethusdt']

    # Добавление константы к независимой переменной
    X = sm.add_constant(X)

    # Проведение регрессионного анализа
    model = sm.OLS(Y, X).fit()

    coefficient_btc = model.params['close_btcusdt']

    return coefficient_btc
