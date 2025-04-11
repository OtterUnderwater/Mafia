import enum

class RoleEnum(enum.StrEnum):
    CIVILIAN = "Civilian"
    MAFIA = "Mafia"
    DON = "Don"
    SHERIFF = "Sheriff"

class StatusEnum(enum.StrEnum):
    ALIVE = "alive"
    DEAD = "dead"

class EliminationReasonEnum(enum.StrEnum):
    VOTED = "voted"
    KILLED = "killed"
    DELETED = "deleted"
