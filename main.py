# створювати звіти:
# ▷ вивести назви кафедр і груп, які до них відносяться

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

# Отримати таблиці
departments_table = Table('departments', metadata, autoload_with=engine)
groups_table = Table('groups', metadata, autoload_with=engine)

query = select([
    departments_table.c.name.label('department_name'),
    groups_table.c.name.label('group_name')
]).select_from(
    departments_table.join(
        groups_table, departments_table.c.id == groups_table.c.department_id
    )
)

# Виконати запит
result = engine.execute(query)

# Вивести результат
for row in result:
    print(f"Кафедра: {row.department_name}, Група: {row.group_name}")

# Закрити з'єднання
result.close()

