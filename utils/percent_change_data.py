from db_utils.create_tables import new_data

def calculate_percent_changes(initial_btc_price, initial_eth_price, current_btc_price, current_eth_price):
    percent_change_eth = ((current_eth_price - initial_eth_price) / initial_eth_price) * 100
    percent_change_btc = ((current_btc_price - initial_btc_price) / initial_btc_price) * 100
    return percent_change_eth, percent_change_btc

def percent_change(coef_btc_to_eth, initial_btc_price, initial_eth_price, current_btc_price, current_eth_price):
    delta_btc = current_btc_price - initial_btc_price
    delta_eth = current_eth_price - initial_eth_price
    delta_eth_own = coef_btc_to_eth * delta_btc
    change_eth_without_coef = delta_eth - delta_eth_own
    percent_change_eth_dependent = (coef_btc_to_eth * delta_btc / initial_eth_price) * 100

    return delta_btc, delta_eth, change_eth_without_coef, percent_change_eth_dependent


def print_results(delta_btc, delta_eth, change_eth_without_coef, percent_change_eth_dependent, current_btc_price,
                  percent_change_global_btc, current_eth_price, percent_change_global_eth):
    print("-" * 35)
    print("Анализ зависимости ETH от BTC:")
    print(f"Изменение BTC: {delta_btc:.2f}$")
    print(f"Изменение ETH: {delta_eth:.2f}$")
    print("-" * 35)
    print(f"Собственное изменение ETH на основе коэффициента наклона: {change_eth_without_coef:.2f}$")
    print(f"Процентное изменение ETH, вызванное изменением BTC с учетом коэффициента наклона: {percent_change_eth_dependent:.2f}%")
    print("-" * 35)
    print("#    Данные для сохранения в БД  #")
    print(f'Фактические данные по BTC : {current_btc_price}$ {percent_change_global_btc:.2f}%')
    print(f'Фактические данные по ETH : {current_eth_price}$ {percent_change_global_eth:.2f}%')
    print("-" * 35)


def save_to_db(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth):
    try:
        new_data(new_time, current_btc_price, current_eth_price, percent_change_btc, percent_change_eth)
        print('Данные сохранены в БД')
        print("-" * 35)
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {str(e)}")
        print("-" * 35)
