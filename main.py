# створювати звіти:
# ▷ вивести назви усіх кафедр

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

# Отримання таблиці departments
departments_table = Table('departments', MetaData(), autoload_with=engine)


def generate_report(table):
    # Створення запиту для виведення назв усіх кафедр
    query = select(table.columns['name'])

    # Виконання запиту
    result = conn.execute(query)

    # Виведення результатів
    print("Назви усіх кафедр:")
    for row in result:
        print(row[0])


# Виклик функції для генерації звіту про кафедри
generate_report(departments_table)

# Закриття з'єднання
conn.close()
