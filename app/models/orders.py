from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk

if TYPE_CHECKING:
    from app.models.buyers import Buyer
    from app.models.products import Product


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int_pk]
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.now(timezone.utc))
    price: Mapped[float] = mapped_column(Integer,
                                         nullable=False)

    buyer: Mapped["Buyer"] = relationship("Buyer", back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem",
                                                          back_populates="order")

    def to_dict(self):
        return {
            "order_id": self.id,
            "created_at": self.created_at,
            "price": self.price,
            "order_items": [
                {
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity
                }
                for item in self.order_items
            ],
        }


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int_pk]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped["Order"] = relationship("Order",
                                          back_populates="order_items")
    product: Mapped["Product"] = relationship("Product",
                                              back_populates="order_items")
