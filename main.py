# створювати звіти:
# ▷ вивести інформацію про всіх викладачів

import json
from sqlalchemy import create_engine, MetaData, Table, select

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Academy'
engine = create_engine(db_url)

# Підключення до бази даних
conn = engine.connect()

# Отримання таблиці teachers
teachers_table = Table('teachers', MetaData(), autoload_with=engine)


def generate_report(table):
    # Створення запиту для виведення інформації про всіх викладачів
    query = select(table)

    # Виконання запиту
    result = conn.execute(query)

    # Виведення результатів
    print("Інформація про всіх викладачів:")
    for row in result:
        print(row)


# Виклик функції для генерації звіту про викладачів
generate_report(teachers_table)

# Закриття з'єднання
conn.close()
