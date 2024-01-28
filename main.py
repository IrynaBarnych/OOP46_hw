# створювати звіти:
# ▷ вивести імена та прізвища викладачів, які читають
# лекції в конкретній групі

import json
from sqlalchemy import create_engine, MetaData, Table, select

# Підключення до бази даних
engine = create_engine("postgresql://username:password@localhost:5432/Academy")

conn = engine.connect()

# Визначення таблиць
metadata = MetaData(bind=engine)
lecturers_table = Table("lecturers", metadata, autoload=True)
groups_table = Table("groups", metadata, autoload=True)
lectures_groups_table = Table("lectures_groups", metadata, autoload=True)


def report_lecturers_for_group(group_name):
    query = (
        select([lecturers_table.c.name, lecturers_table.c.surname])
        .select_from(groups_table.join(lectures_groups_table).join(lecturers_table))
        .where(groups_table.c.name == group_name)
    )
    result = conn.execute(query)

    if result.rowcount == 0:
        print(f"No lecturers found for group {group_name}.")
    else:
        print(f"Lecturers for group {group_name}:")
        for row in result:
            print(row)


# Приклад виклику звіту для групи "Група1"
report_lecturers_for_group("Група1")

# Закриття підключення
conn.close()
