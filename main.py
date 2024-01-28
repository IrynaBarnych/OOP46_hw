# Завдання
# Для бази даних Академія, яку ви розробили в рамках
# курсу «Теорія Баз Даних», створіть додаток для взаємодії
# з базою даних, який дозволяє:
# ■ видаляти рядки з таблиць бази даних;

import json
from sqlalchemy import create_engine, MetaData, Table, delete

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
    print("Доступні колонки для видалення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")

def delete_rows(table):
    columns = table.columns.keys()
    print_columns(columns)

    selected_column_idx = int(input("Введіть номер колонки для умови видалення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("Невірний номер колонки! Видалення відмінено!")
        return

    condition_value = input(f"Введіть значення для умови, {condition_column}: ")

    confirm_update = input("Видалити усі рядки з цієї таблиці? Так/Ні? ")
    if confirm_update.lower() == 'так':
        query = delete(table).where(getattr(table.c, condition_column) == condition_value)
        conn.execute(query)
        conn.commit()
        print("Рядки успішно видалені.")
    else:
        print("Видалення відмінено.")

# Виклик функції для видалення рядків у таблиці faculties
delete_rows(faculties_table)

# Закриття з'єднання
conn.close()

