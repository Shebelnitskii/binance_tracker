import os
import pytest
from utils.data_btc import load_data_btc
from utils.data_eth import load_data_eth
import json


@pytest.fixture
def api_credentials():
    os.environ["API_KEY"] = "kPd3Q9Y0r97kJJT61oS3Gqcg3gk7VL0sJRs6BZCu9EVhtwpZB4BmI7qzTrDauXgS"
    os.environ["API_SECRET_KEY"] = "R0yIKXFasq32SJ1PjFgkMLChcBO6xyPPdgG56LRmiZ0rpNCShfFFW4JH48FSfLLH"
    yield
    del os.environ["API_KEY"]
    del os.environ["API_SECRET_KEY"]


def test_load_data_eth(api_credentials):
    # Вызываем вашу функцию
    load_data_eth()

    # Проверяем, что файл JSON с данными был создан
    assert os.path.exists('utils/data/data_eth.json')

    # Проверяем, что файл JSON не пустой
    assert os.path.getsize('utils/data/data_eth.json') > 0

    # Проверяем, что файл JSON содержит ожидаемые данные
    with open('utils/data/data_eth.json', 'r') as json_file:
        data = json.load(json_file)

    assert all(key in data[0] for key in ['timestamp', 'close'])


def test_load_data_btc(api_credentials):
    # Вызываем вашу функцию
    load_data_btc()

    # Проверяем, что файл JSON с данными был создан
    assert os.path.exists('utils/data/data_btc.json')

    # Проверяем, что файл JSON не пустой
    assert os.path.getsize('utils/data/data_btc.json') > 0

    # Проверяем, что файл JSON содержит ожидаемые данные
    with open('utils/data/data_btc.json', 'r') as json_file:
        data = json.load(json_file)

    assert all(key in data[0] for key in ['timestamp', 'close'])

