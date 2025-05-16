from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from db.database import async_session_maker

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all_filters(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            new_id = res.scalar()
            new_object = await session.get(self.model, new_id)
            return new_object

    async def get_one(self, data: dict):
        async with async_session_maker() as session:
            new_object = await session.get(self.model, data)
            return new_object

    async def get_all(self):
        async with async_session_maker() as session:
           stmt = select(self.model)
           res = await session.execute(stmt)
           return res.scalars().all()

    async def get_all_filters(self, data: dict):
        async with async_session_maker() as session:
            stmt = select(self.model)
            for field, value in data.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def update_one(self, id: int, data: dict):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete_one(self, id: int):
        async with async_session_maker() as session:
            obj_to_delete = await session.get(self.model, id)
            if not obj_to_delete:
                return None
            await session.delete(obj_to_delete)
            await session.commit()
            return obj_to_delete