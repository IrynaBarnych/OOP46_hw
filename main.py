# створювати звіти:
# ▷ вивести назви предметів, які викладає конкретний
# викладач

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
subjects_table = Table('subjects', metadata, autoload_with=engine)
teachers_table = Table('teachers', metadata, autoload_with=engine)
teaching_assignments_table = Table('teaching_assignments', metadata, autoload_with=engine)

# Задайте ім'я конкретного викладача (замініть 'ПІБ_викладача' на реальне ім'я викладача)
teacher_name = 'Олег'

# Зробіть SQL-запит
query = select([subjects_table.c.name]).select_from(
    subjects_table.join(
        teaching_assignments_table,
        subjects_table.c.id == teaching_assignments_table.c.subject_id
    ).join(
        teachers_table,
        teachers_table.c.id == teaching_assignments_table.c.teacher_id
    )
).where(
    teachers_table.c.name == teacher_name
)

# Виконайте запит
result = engine.execute(query)

# Виведіть результат
subject_names = [row.name for row in result]
print(f"Предмети, які викладає викладач {teacher_name}: {', '.join(subject_names)}")

# Закрити з'єднання
result.close()
