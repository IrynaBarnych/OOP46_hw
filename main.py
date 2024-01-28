# Завдання
# Для бази даних Академія, яку ви розробили в рамках
# курсу «Теорія Баз Даних», створіть додаток для взаємодії
# з базою даних, який дозволяє:
# ■ вставляти рядки в таблиці бази даних;

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Academy'
engine = create_engine(db_url)

Base = declarative_base()

# Клас для таблиці Факультети (Faculties)
class Faculty(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dean = Column(String(255), nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    # Зв'язок з таблицею Departments
    departments = relationship('Department', back_populates='faculty')

# Клас для таблиці Кафедри (Departments)
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    financing = Column(Integer, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculties.id'))

    # Зв'язок з таблицею Faculties
    faculty = relationship('Faculty', back_populates='departments')

# Замініть 'postgresql+psycopg2://user:password@localhost:5432/dbname' на ваш реальний DSN
Base.metadata.create_all(engine)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Додавання записів

faculty3 = Faculty(dean='Сидоров С.С.', name='Факультет філосовських наук')
faculty4 = Faculty(dean='Михайлов М.М.', name='Факультет оборонних наук')

faculties = [faculty3, faculty4]

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

for faculty in faculties:
    try:
        session.merge(faculty)
        session.commit()
    except Exception as e:
        print(f"Помилка: {e}")
        session.rollback()

session.close()
