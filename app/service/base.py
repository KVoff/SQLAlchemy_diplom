from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.database import SessionLocal


class BaseService:
    model = None

    @classmethod
    def find_all(cls, **filter_by):
        """Возвращает все записи модели, соответствующие фильтрам."""
        with SessionLocal() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query)
            return result.scalars().all()

    @classmethod
    def get(cls, **filter_by):
        """Возвращает одну запись по фильтрам или None, если не найдено."""
        with SessionLocal() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    def add(cls, **values):
        """Добавляет новую запись в базу данных и возвращает ее."""
        with SessionLocal() as session:
            with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return new_instance

    @classmethod
    def update(cls, filter_by, **values) -> int:
        """Обновляет записи, соответствующие фильтрам, указанными значениями."""
        with SessionLocal() as session:
            # Строим запрос для обновления
            query = (
                update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in
                         filter_by.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            # Выполняем запрос
            result = session.execute(query)
            try:
                session.commit()
                return result.rowcount

            except SQLAlchemyError as e:
                session.rollback()
                raise e

    @classmethod
    def delete(cls, delete_all: bool = False, **filter_by):
        """Удаляет записи, соответствующие фильтрам.
        Требует хотя бы один фильтр или `delete_all=True`.
        Возвращает количество удаленных записей.
        """
        if not delete_all and not filter_by:
            raise ValueError(
                "Необходимо указать хотя бы один параметр для удаления.")

        with SessionLocal() as session:
            with session.begin():
                query = delete(cls.model).filter_by(**filter_by)
                result = session.execute(query)
                try:
                    session.commit()
                    return result.rowcount
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
