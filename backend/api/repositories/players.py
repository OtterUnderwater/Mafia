from api.repository import SQLAlchemyRepository
from db.models import Player

class PlayerRepository(SQLAlchemyRepository):
    model = Player

