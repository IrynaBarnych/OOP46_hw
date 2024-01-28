# створювати звіти:
# ▷ вивести назви кафедр, на яких викладається конкретна дисципліна

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
departments_table = Table('departments', metadata, autoload_with=engine)
subjects_table = Table('subjects', metadata, autoload_with=engine)
teaching_assignments_table = Table('teaching_assignments', metadata, autoload_with=engine)

# Задайте ім'я конкретної дисципліни (замініть 'Назва_дисципліни' на реальну назву)
subject_name = 'Математика'

# Зробіть SQL-запит
query = select([departments_table.c.name]).select_from(
    departments_table.join(
        teaching_assignments_table,
        departments_table.c.id == teaching_assignments_table.c.department_id
    ).join(
        subjects_table,
        subjects_table.c.id == teaching_assignments_table.c.subject_id
    )
).where(
    subjects_table.c.name == subject_name
)

# Виконайте запит
result = engine.execute(query)

# Виведіть результат
department_names = [row.name for row in result]
print(f"Кафедри, на яких викладається дисципліна {subject_name}: {', '.join(department_names)}")

# Закрити з'єднання
result.close()
