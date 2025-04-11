from api.repository import SQLAlchemyRepository
from db.models import Game

class GameRepository(SQLAlchemyRepository):
    model = Game

