from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    # Получаем значения переменных окружения
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Проверяем, что переменные определены
    if None in (db_host, db_port, db_name, db_user, db_password):
        raise ValueError("Один или несколько параметров для подключения к базе данных не установлены.")

    # Преобразуем порт в целое число (если он задан)
    if db_port is not None:
        db_port = int(db_port)


    # Создаем подключение к базе данных
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    # Проверяем подключение
    try:
        connection = engine.connect()
        print("Подключение к базе данных успешно установлено.")
        print("-" * 35)
        return engine, connection
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {str(e)}")
        print("-" * 35)