# створювати звіти:
# ▷ відобразити кафедру з максимальною кількістю груп

import json
from sqlalchemy import create_engine, MetaData, Table, select, func

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

# Зробити SQL-запит
query = select([
    departments_table.c.name,
    func.count().label('group_count')
]).select_from(
    departments_table.join(
        groups_table, departments_table.c.id == groups_table.c.department_id
    )
).group_by(
    departments_table.c.id
).order_by(
    func.count().desc()
).limit(1)

# Виконати запит
result = engine.execute(query)

# Вивести результат
for row in result:
    print(f"Кафедра: {row.name}, Кількість груп: {row.group_count}")

# Закрити з'єднання
result.close()
