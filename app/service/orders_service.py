from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models import Order, OrderItem, Product, Buyer

from app.schemas.orders import SOrderCreate
from app.schemas.request import RbBuyer
from app.service.base import BaseService


class OrderService(BaseService):
    model = Order

    @classmethod
    def find_orders_by_buyer(cls, buyer: RbBuyer):
        # Проверка: если оба поля None, выдать исключение с сообщением
        if buyer.id is None and buyer.phone_number is None:
            raise HTTPException(
                status_code=400,
                detail="Введите либо id, либо номер телефона"
            )

        # Проверка: если введены оба поля, вернуть сообщение об ошибке
        if buyer.id is not None and buyer.phone_number is not None:
            raise HTTPException(
                status_code=400,
                detail="Введите либо id, либо номер телефона, но не оба"
            )

        with SessionLocal() as session:
            # Проверка: существует ли покупатель с данным id или phone_number
            buyer_query = select(Buyer).filter(
                (Buyer.id == buyer.id) if buyer.id is not None else (
                        Buyer.phone_number == buyer.phone_number)
            )
            buyer_instance = session.execute(buyer_query).scalar_one_or_none()

            if buyer_instance is None:
                raise HTTPException(
                    status_code=404,
                    detail="Такого покупателя нет"
                )

            query = (
                select(cls.model)
                .options(
                    joinedload(cls.model.order_items)
                    .joinedload(OrderItem.product)
                )
                .filter(cls.model.buyer_id == buyer_instance.id)
            )




            result = session.execute(query).unique()
            return result.scalars().all()

    @classmethod
    def create_order(cls, order_data: SOrderCreate):
        with SessionLocal() as session:
            # Проверка существования покупателя
            buyer = session.query(Buyer).filter(
                Buyer.id == order_data.buyer_id).first()
            if not buyer:
                raise HTTPException(status_code=404,
                                    detail="Покупатель не найден")

            # Инициализация общей стоимости заказа
            total_price = 0
            order_items = []

            # Проверка и добавление продуктов в заказ
            for item in order_data.items:
                product = session.query(Product).filter(
                    Product.id == item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404,
                                        detail=f"Продукт с ID {item.product_id} не найден")

                # Проверка наличия товара
                if product.count < item.quantity:
                    raise HTTPException(status_code=400,
                                        detail=f"Недостаточно товара '{product.name}' в наличии. Доступно: {product.count}, запрашивается: {item.quantity}")

                # Рассчитываем общую стоимость
                total_price += product.price * item.quantity

                # Создаем элементы заказа
                order_item = OrderItem(product_id=item.product_id,
                                       quantity=item.quantity)
                order_items.append((order_item,
                                    product))  # Сохраняем элемент заказа и продукт

            # Создаем новый заказ
            order = Order(buyer_id=order_data.buyer_id, price=total_price)
            session.add(order)
            session.flush()  # Получаем ID нового заказа перед добавлением элементов

            # Добавляем все элементы заказа к заказу и обновляем количество товара
            for order_item, product in order_items:
                order_item.order_id = order.id  # Устанавливаем ID заказа для каждого элемента
                session.add(order_item)

                # Уменьшаем количество товара на складе
                product.count -= order_item.quantity
                session.add(
                    product)  # Добавляем продукт для отслеживания изменений

            session.commit()
            return order.to_dict()  # Возвращаем созданный заказ
