import json
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from db_utils.connect_db import connect_db

# Создание базового класса для объявления моделей таблиц
Base = declarative_base()


# Определение моделей таблицы для ETH и BTC
class BinanceData(Base):
    __tablename__ = 'binance_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True)
    price_ethusdt = Column(Float)
    price_btcusdt = Column(Float)
    change_ethusdt = Column(Float, nullable=True)
    change_btcusdt = Column(Float, nullable=True)


def create_tables():
    """Заполнение БД данными из historical_data.json"""
    try:
        # Создание подключения к базе данных
        engine, connection = connect_db()

        # Создание таблиц в базе данных (если они ещё не существуют)
        Base.metadata.create_all(engine)

        # Создание сессии для выполнения запросов
        Session = sessionmaker(bind=engine)
        session = Session()

        # Загрузка данных из JSON и сохранение их в базе данных
        with open('utils/data/historical_data.json', 'r') as data_file:
            data = json.load(data_file)
            for entry in data:
                # Преобразование
                timestamp_datetime = datetime.utcfromtimestamp(entry['timestamp'] / 1000.0)
                # Форматирование даты и времени в строку
                formatted_datetime = timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    # Проверяем json на наличие новых временных меток и данных, для добавления в таблицу
                    existing_data = session.query(BinanceData).filter_by(timestamp=formatted_datetime).one()
                except NoResultFound:
                    # Если временной метки нет, то данные сохраняются в таблицу
                    binance_data = BinanceData(
                        timestamp=formatted_datetime,
                        price_btcusdt=entry['close_btcusdt'],
                        price_ethusdt=entry['close_ethusdt'],
                        change_btcusdt=entry['change_btcusdt'],
                        change_ethusdt=entry['change_ethusdt']
                    )
                    session.add(binance_data)

        # Сохранение изменений
        session.commit()

        # Закрытие сессии
        session.close()

    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {str(e)}")


def new_data(timestamp, data_btc, data_eth, change_btc, change_eth):
    """Добавление новых данных  в БД"""
    # Создание подключения к базе данных
    engine, connection = connect_db()

    # Создание сессии для добавления новых данных в БД
    Session = sessionmaker(bind=engine)
    session = Session()

    binance_data = BinanceData(
        timestamp=timestamp,
        price_btcusdt=data_btc,
        price_ethusdt=data_eth,
        change_btcusdt=change_btc,
        change_ethusdt=change_eth
    )

    session.add(binance_data)

    # Сохранение изменений
    session.commit()

    # Закрытие сессии
    session.close()
