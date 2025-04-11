from api.repository import SQLAlchemyRepository
from db.models import PlayerStatus

class PlayerStatusRepository(SQLAlchemyRepository):
    model = PlayerStatus