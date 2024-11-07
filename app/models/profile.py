from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk

if TYPE_CHECKING:
    from app.models.buyers import Buyer

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int_pk]
    bio: Mapped[str]
    avatar_url: Mapped[Optional[str]]

    # ForeignKey для связи с Buyer
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"), unique=True)

    # Связь с User
    buyer: Mapped["Buyer"] = relationship(
        "Buyer", back_populates="profile", uselist=False
    )
