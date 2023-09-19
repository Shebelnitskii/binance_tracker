from utils.coefficient_regression_line import load_coefficient_btc
from utils.save_data_btc_eth import save_changes_eth_btc
from utils.get_data import get_btc_price, get_eth_price
from db_utils.create_tables import create_tables, new_data
from datetime import datetime, timedelta
import time


def user_interaction():
    """Основное тело программы"""
    ### Проверка заполнености БД
    save_changes_eth_btc()
    create_tables()
    coef_btc_to_eth = load_coefficient_btc()
    ### Начало цикла
    while True:
        time_now = datetime.now()
        initial_eth_price = get_eth_price()
        initial_btc_price = get_btc_price()
        print(f"Фактические данные по ETH: {initial_eth_price}")
        print(f"Фактические данные по BTC: {initial_btc_price}")
        print("-" * 35)
        while True:
            # Ждем 60 секунд
            time.sleep(60)
            new_time = datetime.now()

            # Получаем новое значение
            current_eth_price = get_eth_price()
            current_btc_price = get_btc_price()

            # Вычисляем процентное изменение
            percent_change_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100
            percent_change_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100
            if abs(percent_change_eth) >= 1:
                # Расчет изменения BTC и ETH
                delta_btc = current_btc_price - initial_btc_price
                delta_eth = current_eth_price - initial_eth_price

                # Расчет собственного изменения ETH на основе коэффициента наклона
                delta_eth_own = coef_btc_to_eth * delta_btc

                # Расчет собственного процентного изменения ETH с учётом коэффициента наклона
                percent_change_eth_dependent = (coef_btc_to_eth * delta_btc / initial_eth_price) * 100

                # Расчет глобального процентного изменения ETH и BTC
                percent_change_global_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100
                percent_change_global_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100

                # Вывод информации
                print("Анализ зависимости ETH от BTC:")
                print("-" * 35)
                print(f"Изменение BTC: {delta_btc:.2f}$")
                print(f"Изменение ETH: {delta_eth:.2f}$")
                print(f"Собственное изменение ETH на основе коэффициента наклона: {delta_eth_own:.2f}$")
                print(
                    f"Процентное изменение ETH, вызванное изменением BTC с учетом коэффициента наклона: {percent_change_eth_dependent:.2f}%")
                print("-" * 35)
                print("#    Данные для сохранения в БД  #")
                print("-" * 35)
                print(f'Фактические данные по BTC : {current_btc_price}$ {percent_change_global_btc:.2f}%')
                print(f'Фактические данные по ETH : {current_eth_price}$ {percent_change_global_eth:.2f}%')
                try:
                    print("-" * 35)
                    new_data(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth)
                    print('Данные сохранены в БД\n')
                    print("-" * 35)
                    print("\n" * 5)
                    break
                except Exception as e:
                    print(f"Ошибка при подключении к базе данных: {str(e)}")

            time_difference = new_time - time_now
            # Проверяем, равна ли разница 1 часу
            if time_difference >= timedelta(hours=1):
                print("В течении часа у ETHUSDT не было изменений на 1%\nДанные по ETH не будут сохранены в таблицу")
                time_now = new_time
