# Завдання
# Для бази даних Академія, яку ви розробили в рамках
# курсу «Теорія Баз Даних», створіть додаток для взаємодії
# з базою даних, який дозволяє:
# ■ оновлювати рядків у таблицях бази даних;

import json
from sqlalchemy import create_engine, MetaData, Table, update

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

# Отримання таблиці faculties
faculties_table = Table('faculties', MetaData(), autoload_with=engine)

def print_columns(columns):
    print("Доступні колонки для оновлення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")

def update_rows(table):
    columns = table.columns.keys()
    print_columns(columns)

    selected_column_idx = int(input("Введіть номер колонки для оновлення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("Невірний номер колонки!")

    condition_value = input(f"Введіть значення для умови, {condition_column}: ")
    new_values = {}

    # Введення нових значень для кожної колонки
    for column in columns:
        value = input(f"Введіть нове значення для колонки {column}: ")
        new_values[column] = value

    confirm_update = input("Оновити усі рядки? Так/Ні? ")
    if confirm_update.lower() == 'так':
        query = update(table).where(getattr(table.c, condition_column) == condition_value).values(new_values)
        conn.execute(query)
        conn.commit()

# Виклик функції для оновлення рядків у таблиці faculties
update_rows(faculties_table)

# Закриття з'єднання
conn.close()
