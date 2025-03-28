from __future__ import annotations

from uuid import UUID

from tanks.entity.base import BaseEntity
from tanks.world.base import BaseWorld


class World(BaseWorld):
    entity_manager: EntityManager

    def __init__(self) -> None:
        super().__init__()
        self.entity_manager = EntityManager()

    def add_entity(self, entity: BaseEntity) -> None:
        self.entity_manager.add_entity(entity)

    def tick(self) -> None:
        self.entity_manager.tick()


class EntityManager:
    def __init__(self) -> None:
        self.entities: dict[UUID, BaseEntity] = {}

    def add_entity(self, entity: BaseEntity) -> None:
        self.entities[entity.uuid] = entity

    def tick(self) -> None:
        for entity in self.entities.values():
            entity.tick()
