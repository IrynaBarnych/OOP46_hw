# створювати звіти:
# ▷ вивести інформацію про всі навчальні групи,

from sqlalchemy import create_engine, MetaData, Table, select
import json

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

# Отримання таблиці groups
groups_table = Table('groups', MetaData(), autoload_with=engine)


def generate_report(table):
    # Створення запиту для виведення інформації про всі навчальні групи
    query = select(table)

    # Виконання запиту
    result = conn.execute(query)

    # Виведення результатів
    print("Інформація про всі навчальні групи:")
    for row in result:
        print(row)


# Виклик функції для генерації звіту про навчальні групи
generate_report(groups_table)

# Закриття з'єднання
conn.close()


