# створювати звіти:
# ▷ вивести назву предмету, за яким читається найбільше лекцій

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

# Отримання таблиць
lectures_table = Table('lectures', metadata, autoload_with=engine)
subjects_table = Table('subjects', metadata, autoload_with=engine)

# Зробіть SQL-запит
query = (
    select([
        subjects_table.c.name.label('subject_name'),
        func.count().label('lecture_count')
    ])
    .select_from(
        lectures_table.join(
            subjects_table,
            lectures_table.c.subject_id == subjects_table.c.id
        )
    )
    .group_by('subject_name')
    .order_by(func.count().desc())
    .limit(1)
)

# Виконайте запит
result = engine.execute(query)

# Виведіть результат
for row in result:
    print(f"Найбільше лекцій за предметом: {row.subject_name}, Кількість лекцій: {row.lecture_count}")

# Закрити з'єднання
result.close()
