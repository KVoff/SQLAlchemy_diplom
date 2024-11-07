from typing import List, TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_uniq, str_null_true

if TYPE_CHECKING:
    from app.models.orders import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str_null_true]
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0)

    # Связь "многие ко многим" с OrderItem (например, для заказа продукта)
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "count": self.count,
        }
