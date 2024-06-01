from enum import Enum


class CollisionDirection(Enum):
    HORIZONTAL = "x"
    VERTICAL = "y"


class SpriteType(Enum):
    PLAYER = 0
    CAR = 1
    OBJECT = 2