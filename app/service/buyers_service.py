from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.service.base import BaseService
from app.models.buyers import Buyer


class BuyerService(BaseService):
    model = Buyer

    @classmethod
    def find_full_data(cls, buyer_id: int):
        with SessionLocal() as session:
            # Запрос для получения покупателя и его адресов
            query = (
                select(cls.model)
                .options(joinedload(cls.model.addresses))
                .filter_by(id=buyer_id)
            )

            result = session.execute(query).unique()
            buyer_info = result.scalar_one_or_none()

            # Проверка на существование покупателя
            if not buyer_info:
                return None

            return buyer_info.to_dict()
