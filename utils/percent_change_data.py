from db_utils.create_tables import new_data


def percent_change(new_time, coef_btc_to_eth, current_btc_price, current_eth_price, initial_btc_price, initial_eth_price):

    # Вычисляем процентное изменение
    percent_change_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100
    percent_change_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100

    if abs(percent_change_eth) >= 1:
        # Расчет изменения BTC и ETH
        delta_btc = current_btc_price - initial_btc_price
        delta_eth = current_eth_price - initial_eth_price

        # Расчет собственного изменения ETH на основе коэффициента наклона
        delta_eth_own = coef_btc_to_eth * delta_btc
        change_eth_without_coef = delta_eth - delta_eth_own

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
        print(f"Собственное изменение ETH на основе коэффициента наклона: {change_eth_without_coef:.2f}$")
        print(
            f"Процентное изменение ETH, вызванное изменением BTC с учетом коэффициента наклона: {percent_change_eth_dependent:.2f}%")
        print("-" * 35)
        print("#    Данные для сохранения в БД  #")
        print("-" * 35)
        print(f'Фактические данные по BTC : {current_btc_price}$ {percent_change_global_btc:.2f}%')
        print(f'Фактические данные по ETH : {current_eth_price}$ {percent_change_global_eth:.2f}%')
        print("-" * 35)
        try:
            print("-" * 35)
            new_data(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth)
            print('Данные сохранены в БД')
            print("-" * 35)
            return False
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {str(e)}")
            print("-" * 35)
