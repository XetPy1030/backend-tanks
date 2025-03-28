import uuid
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tanks.world.base import BaseWorld

class BaseEntity:
    def __init__(self, x: float, y: float, world: 'BaseWorld', entity_id: UUID | None = None) -> None:
        self.uuid: UUID = entity_id if entity_id is not None else uuid.uuid4()
        self.x: float = x
        self.y: float = y
        self.world = world
    
    def tick(self) -> None:
        pass
