import pytest
from utils.percent_change_data import calculate_percent_changes, percent_change, save_to_db


def test_calculate_percent_changes():
    # Задаем начальные и текущие значения
    initial_btc_price = 10000.0
    initial_eth_price = 200.0
    current_btc_price = 10500.0
    current_eth_price = 220.0

    # Вычисляем ожидаемые процентные изменения
    expected_percent_change_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100
    expected_percent_change_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100

    # Вызываем тестируемую функцию
    percent_change_eth, percent_change_btc = calculate_percent_changes(initial_btc_price, initial_eth_price,
                                                                       current_btc_price, current_eth_price)

    # Проверяем, что результаты совпадают с ожидаемыми значениями
    assert percent_change_eth == expected_percent_change_eth
    assert percent_change_btc == expected_percent_change_btc


def test_percent_change():
    # Задаем начальные и текущие значения, а также коэффициент
    initial_btc_price = 10000.0
    initial_eth_price = 200.0
    current_btc_price = 10500.0
    current_eth_price = 220.0
    coef_btc_to_eth = 0.5

    # Вычисляем ожидаемые значения изменений и процентов
    expected_delta_btc = current_btc_price - initial_btc_price
    expected_delta_eth = current_eth_price - initial_eth_price
    expected_delta_eth_own = coef_btc_to_eth * expected_delta_btc
    expected_change_eth_without_coef = expected_delta_eth - expected_delta_eth_own
    expected_percent_change_eth_dependent = (coef_btc_to_eth * expected_delta_btc / initial_eth_price) * 100
    expected_percent_change_global_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100
    expected_percent_change_global_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100

    # Вызываем тестируемую функцию
    delta_btc, delta_eth, change_eth_without_coef, percent_change_eth_dependent, percent_change_global_btc, \
    percent_change_global_eth = percent_change(coef_btc_to_eth, initial_btc_price, initial_eth_price,
                                               current_btc_price, current_eth_price)

    # Проверяем, что результаты совпадают с ожидаемыми значениями
    assert delta_btc == expected_delta_btc
    assert delta_eth == expected_delta_eth
    assert change_eth_without_coef == expected_change_eth_without_coef
    assert percent_change_eth_dependent == expected_percent_change_eth_dependent
    assert percent_change_global_btc == expected_percent_change_global_btc
    assert percent_change_global_eth == expected_percent_change_global_eth

def test_save_to_db():
    # Данные для теста
    new_time = "2023-09-22 12:00:00"
    current_btc_price = 10000.0
    current_eth_price = 200.0
    percent_change_btc = 5.0
    percent_change_eth = 10.0

    assert save_to_db(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth) is False
