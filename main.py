# створювати звіти:
# ▷ вивести назви груп, що належать до конкретного
# факультету

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
faculties_table = Table('faculties', metadata, autoload_with=engine)
groups_table = Table('groups', metadata, autoload_with=engine)
departments_table = Table('departments', metadata, autoload_with=engine)

# Задайте ім'я конкретного факультету (замініть 'Назва_факультету' на реальну назву)
faculty_name = 'Факультет природничих наук'

query = select([groups_table.c.name]).select_from(
    groups_table.join(
        departments_table,
        groups_table.c.department_id == departments_table.c.id
    ).join(
        faculties_table,
        faculties_table.c.id == departments_table.c.faculty_id
    )
).where(
    faculties_table.c.name == faculty_name
)

# Виконайте запит
result = engine.execute(query)

# Виведіть результат
group_names = [row.name for row in result]
print(f"Групи, що належать до факультету {faculty_name}: {', '.join(group_names)}")

# Закрити з'єднання
result.close()
