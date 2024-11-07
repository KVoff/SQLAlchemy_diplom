import pytest
import logging
from datetime import date, datetime, timezone
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.models.buyers import Base, Buyer, Address
from app.models.orders import Order


# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test/test_logs.log', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)

# Настройка тестового окружения
engine = create_engine("sqlite:///test/test_database.db", echo=True)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(setup_database):
    session = Session()
    yield session
    session.close()


def test_create_buyer(session):
    # Создание покупателя
    buyer = Buyer(
        first_name="Брюс",
        last_name="Ли",
        date_of_birth=date(2000, 9, 8),
        phone_number="+79991234777",
        email="bl_unique_to_dict@example.com"
    )
    session.add(buyer)
    session.commit()
    assert buyer.id is not None
    logger.info("Buyer created successfully.")


def test_create_address(session):
    # Создание адреса
    address = Address(street="Stroiteley", house_number="21")
    session.add(address)
    session.commit()
    assert address.id is not None
    logger.info("Address created successfully.")


def test_buyer_to_dict(session):
    # Проверка to_dict
    buyer = Buyer(
        first_name="Брюс",
        last_name="Ли",
        date_of_birth=date(2000, 9, 10),
        phone_number="+79991234567",
        email="bl@example.com"
    )
    address = Address(street="Stroiteley", house_number="21")
    session.add_all([buyer, address])
    buyer.addresses.append(address)
    session.commit()

    buyer_dict = buyer.to_dict()
    assert buyer_dict["first_name"] == "Брюс"
    assert buyer_dict["address"][0]["street"] == "Stroiteley"
    logger.info("Buyer to_dict method passed.")


def test_update_buyer_phone_number(session):
    # Обновление номера телефона покупателя
    buyer = session.execute(select(Buyer)).scalars().first()
    buyer.phone_number = "+79998887766"
    session.commit()
    updated_buyer = session.get(Buyer, buyer.id)
    assert updated_buyer.phone_number == "+79998887766"
    logger.info("Buyer phone number updated successfully.")


def test_delete_buyer(session):
    # Удаление покупателя
    buyer = session.execute(select(Buyer)).scalars().first()
    session.delete(buyer)
    session.commit()
    deleted_buyer = session.get(Buyer, buyer.id)
    assert deleted_buyer is None
    logger.info("Buyer deleted successfully.")


def test_order_creation(session):
    # Создание заказа для покупателя
    buyer = Buyer(
        first_name="Брюс",
        last_name="Ли",
        date_of_birth=date(2000, 9, 8),
        phone_number="+79991238887",
        email="bl_unique_to_dict@example.com"
    )
    order = Order(created_at=datetime.now(timezone.utc), price=100.0, buyer=buyer)
    session.add(order)
    session.commit()
    assert order.id is not None
    logger.info("Order created successfully.")


def test_order_to_dict(session):
    # Проверка метода to_dict для Order
    order = session.execute(select(Order)).scalars().first()
    order_dict = order.to_dict()
    assert "order_id" in order_dict
    assert "order_items" in order_dict
    logger.info("Order to_dict method passed.")

