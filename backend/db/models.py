from typing import Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db.sql_enums import RoleEnum, StatusEnum, EliminationReasonEnum

class Player(Base):
    __tablename__ = 'player'
    nickname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    player_status: Mapped[list["PlayerStatus"]] = relationship(
        "PlayerStatus",
        back_populates="player"
    )

class Game(Base):
    __tablename__ = 'game'
    id_master: Mapped[Optional[int]]
    player_status: Mapped[list["PlayerStatus"]] = relationship(
        "PlayerStatus",
        back_populates="game"
    )

class PlayerStatus(Base):
    __tablename__ = 'player_status'
    id_player: Mapped[int] = mapped_column(ForeignKey('player.id'))
    id_game: Mapped[int] = mapped_column(ForeignKey('game.id'))
    # Связь многие-к-одному
    player: Mapped["Player"] = relationship(
        "Player",
        back_populates="player_status"
    )
    game: Mapped["Game"] = relationship(
        "Game",
        back_populates="player_status"
    )
    role: Mapped[Optional[RoleEnum]]
    fouls: Mapped[Optional[int]]
    status: Mapped[StatusEnum]  = mapped_column(
        default=StatusEnum.ALIVE
    )
    elimination_reason: Mapped[Optional[EliminationReasonEnum]]