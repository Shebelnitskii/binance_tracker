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
    ### Начало цикла
    while True:
        time_now = datetime.now()
        initial_eth_price = get_eth_price()
        initial_btc_price = get_btc_price()
        print(f"Стартовое значение ETH: {initial_eth_price}")
        print(f"Стартовое значение BTC: {initial_btc_price}")
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
            if percent_change_eth >= 1 or percent_change_eth <= -1:
                initial_eth_price = current_eth_price
                print(f'Новое значение ETH: {current_eth_price}')
                print(f'Новое значение BTC: {current_btc_price}')
                print(f'Изменение ETH: {percent_change_eth:.2f}%')
                print(f'Изменение BTC: {percent_change_btc:.2f}%')
                try:
                    new_data(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth)
                    print('Данные сохранены в БД')
                except Exception as e:
                    print(f"Ошибка при подключении к базе данных: {str(e)}")

            time_difference = new_time - time_now
            # Проверяем, равна ли разница 1 часу
            if time_difference >= timedelta(hours=1):
                print("В течении часа у ETHUSDT не было изменений на 1%\nДанные по ETH не будут сохранены в таблицу")
                time_now = new_time
