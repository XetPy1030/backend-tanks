from __future__ import annotations

from uuid import UUID

from tanks.entity.base import BaseEntity


class BaseWorld:
    def __init__(self, width: float = 100.0, height: float = 100.0):
        self.width = width
        self.height = height
        self.entity_manager = EntityManager()

    def tick(self) -> None:
        self.entity_manager.tick()

        # Проверяем и ограничиваем позиции всех сущностей в пределах мира
        for entity in list(self.entity_manager.entities.values()):
            # Проверяем касание краев и вызываем соответствующее событие
            if entity.x <= entity.size or entity.x >= self.width - entity.size or \
               entity.y <= entity.size or entity.y >= self.height - entity.size:
                entity.on_world_boundary()


    def add_entity(self, entity: BaseEntity) -> None:
        """Добавляет сущность в мир"""
        self.entity_manager.add_entity(entity)

    def remove_entity(self, entity: BaseEntity) -> None:
        """Удаляет сущность из мира"""
        self.entity_manager.remove_entity(entity)


class EntityManager:
    def __init__(self) -> None:
        self.entities: dict[UUID, BaseEntity] = {}

    def add_entity(self, entity: BaseEntity) -> None:
        self.entities[entity.uuid] = entity

    def tick(self) -> None:
        for entity in self.entities.values():
            entity.tick()

    def remove_entity(self, entity: BaseEntity) -> None:
        del self.entities[entity.uuid]

