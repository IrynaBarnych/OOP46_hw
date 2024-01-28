# передбачити можливість входу з різними рівнями доступу.
# Наприклад: доступ лише для читання, доступ
# для читання та запис, доступ для читання певних таблиць.

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
metadata = MetaData()

# Отримання таблиць
lectures_table = Table('lectures', metadata, autoload_with=engine)
subjects_table = Table('subjects', metadata, autoload_with=engine)


user_name = 'user1'
user_role = 'read_write'


if user_role == 'read_only':
    lectures_query = select([lectures_table])
    subjects_query = select([subjects_table])
elif user_role == 'read_write':
    lectures_query = select([lectures_table])
    subjects_query = select([subjects_table])
    # Додайте інші запити для запису, якщо потрібно
elif user_role == 'read_subjects':
    lectures_query = select([lectures_table])
    subjects_query = select([subjects_table.c.name, subjects_table.c.id])
else:
    raise ValueError("Невідомий рівень доступу")

# Виконайте запити
lectures_result = engine.execute(lectures_query)
subjects_result = engine.execute(subjects_query)


print("Результат запиту до таблиці lectures:")
for row in lectures_result:
    print(row)

print("\nРезультат запиту до таблиці subjects:")
for row in subjects_result:
    print(row)

# Закрити з'єднання
lectures_result.close()
subjects_result.close()
