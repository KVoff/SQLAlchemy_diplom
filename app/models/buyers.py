from datetime import date
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, str_uniq, int_pk, str_null_true

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.orders import Order


# Определяем промежуточную модель для связи "многие ко многим"
# между покупателями и адресами
class BuyerAddress(Base):
    __tablename__ = "buyer_address"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("buyers.id"), primary_key=True
    )
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id"), primary_key=True
    )


# Основная модель Buyer для реализации связей
class Buyer(Base):
    __tablename__ = "buyers"
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column(Date)
    special_notes: Mapped[str_null_true]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]

    # Связь "многие ко многим" с Address через промежуточную таблицу
    # user_address
    addresses: Mapped[List["Address"]] = relationship(
        "Address", secondary="buyer_address", back_populates="buyers"
    )
    # Связь "один ко многим" с Orders
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="buyer", cascade="all, delete"
    )
    # Связь "один к одному" с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="buyer", uselist=False
    )

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r})")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "special_notes": self.special_notes,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": [address.to_dict() for address in self.addresses],
        }


# Модель Address для связи "многие ко многим" с User
class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int_pk]
    street: Mapped[str]
    house_number: Mapped[str]

    # Связь "многие ко многим" с User через промежуточную таблицу user_address
    buyers: Mapped[List["Buyer"]] = relationship(
        "Buyer", secondary="buyer_address", back_populates="addresses"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "street": self.street,
            "house_number": self.house_number,
        }
