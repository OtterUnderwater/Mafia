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
    async def update_one(self, id: int, data: dict):
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

    async def get_by_game_id(self, id_game: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id_game == id_game)
            result = await session.execute(stmt)
            return result.scalars().all()

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

