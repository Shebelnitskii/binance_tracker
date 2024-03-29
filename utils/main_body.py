from utils.coefficient_regression_line import load_coefficient_btc
from utils.save_data_btc_eth import save_changes_eth_btc
from utils.get_data import get_btc_price, get_eth_price
from utils.percent_change_data import percent_change, print_results, save_to_db, calculate_percent_changes
from db_utils.create_tables import create_tables
from datetime import datetime, timedelta
import time


def user_interaction():
    """Основное тело программы"""
    # Проверка заполнености БД
    save_changes_eth_btc()
    create_tables()
    coef_btc_to_eth = load_coefficient_btc()
    time_now = datetime.now()
    initial_eth_price = get_eth_price()
    initial_btc_price = get_btc_price()
    print(f"Фактические данные по BTC: {initial_btc_price}")
    print(f"Фактические данные по ETH: {initial_eth_price}")
    # Начало цикла
    while True:
        # Ждем 60 секунд
        time.sleep(60)
        new_time = datetime.now()

        # Получаем новое значение
        current_eth_price = get_eth_price()
        current_btc_price = get_btc_price()
        percent_change_btc, percent_change_eth = calculate_percent_changes(initial_btc_price, initial_eth_price,
                                                                           current_btc_price, current_eth_price)
        if abs(percent_change_eth) >= 0.01:
            delta_btc, delta_eth, change_eth_without_coef, percent_change_eth_dependent = percent_change(
                coef_btc_to_eth, initial_btc_price, initial_eth_price,
                current_btc_price, current_eth_price)

            print_results(delta_btc, delta_eth, change_eth_without_coef, percent_change_eth_dependent,
                          current_btc_price, percent_change_btc, current_eth_price,
                          percent_change_eth)

            save_to_db(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth)
            initial_eth_price = current_eth_price
            initial_btc_price = current_btc_price

        time_difference = new_time - time_now

        # Проверяем, равна ли разница 1 часу
        if time_difference >= timedelta(hours=1):
            print("В течении часа у ETHUSDT не было изменений на 1%\nДанные по ETH не будут сохранены в таблицу")
            print("-" * 35)
            time_now = new_time
