import pytest
import time
import logging
from datetime import date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.models.buyers import Base, Buyer


# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test/test_time.log', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)

# Создание движка и сессии для тестов
DATABASE_URL = "sqlite:///test_time_sqlite.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    # Настройка тестовой базы данных перед всеми тестами
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()  # Откат изменений после всех тестов
    session.close()
    Base.metadata.drop_all(bind=engine)

# Тесты CRUD для покупателей
def test_create_buyers(session):
    start_time = time.time()
    buyers = [
        Buyer(
            first_name=f"FirstName{i}",
            last_name=f"LastName{i}",
            date_of_birth=date(1990, 1, 1),
            special_notes=f"Notes {i}",
            phone_number=f"+123456789{i}",
            email=f"test_user{i}@example.com"
        ) for i in range(100_000)
    ]
    session.add_all(buyers)
    session.commit()
    logger.info(f"Create {len(buyers)} buyers: {time.time() - start_time} seconds")

def test_read_buyers(session):
    start_time = time.time()
    buyers = session.execute(select(Buyer)).scalars().all()
    logger.info(f"Read {len(buyers)} buyers: {time.time() - start_time} seconds")

def test_update_buyers(session):
    start_time = time.time()
    buyers = session.execute(select(Buyer)).scalars().all()
    for buyer in buyers:
        buyer.first_name = f"Updated_{buyer.first_name}"
    session.commit()
    logger.info(f"Update {len(buyers)} buyers: {time.time() - start_time} seconds")

def test_delete_buyers(session):
    start_time = time.time()
    session.query(Buyer).delete()
    session.commit()
    logger.info(f"Delete all buyers: {time.time() - start_time} seconds")



# def test_delete_buyers_by_one(session):
#     start_time = time.time()
#     # Получаем все записи в таблице Buyer
#     buyers = session.query(Buyer).all()
#     # Удаляем каждый объект по одному
#     for buyer in buyers:
#         session.delete(buyer)
#     session.commit()
#     logger.info(f"Delete all buyers: {time.time() - start_time} seconds")






