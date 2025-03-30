from __future__ import annotations

import uuid
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tanks.world.base import BaseWorld

class BaseEntity:
    """
    Базовый класс для всех сущностей в игре.
    
    Каждая сущность имеет:
    - Уникальный идентификатор (uuid)
    - Позицию в мире (x, y)
    - Ссылку на игровой мир (world)
    - Размер (size) - определяет радиус круглой коллизии сущности
    """
    def __init__(self, x: float, y: float, world: 'BaseWorld', entity_id: UUID | None = None, size: float = 1.0, **kwargs) -> None:
        self.uuid: UUID = entity_id if entity_id is not None else uuid.uuid4()
        self.x: float = x
        self.y: float = y
        self.world: BaseWorld = world
        self.size: float = size
        self._removed: bool = False
    
    def tick(self) -> None:
        # Проверяем коллизии со всеми сущностями в мире
        for entity in self.world.entity_manager.entities.values():
            if entity.uuid == self.uuid:
                continue
                
            # Вычисляем расстояние между центрами сущностей
            dx = self.x - entity.x
            dy = self.y - entity.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            # Проверяем пересечение коллизий
            if distance < (self.size + entity.size):
                self.on_collision(entity)
    
    def on_collision(self, other: BaseEntity) -> None:
        """Вызывается при столкновении с другой сущностью"""
        pass

    def on_remove(self) -> None:
        """Вызывается перед удалением сущности из мира"""
        pass

    def on_world_boundary(self) -> None:
        """Вызывается при выходе сущности за границы мира"""
        pass

    def remove(self) -> None:
        """Удаляет сущность из мира"""
        if not self._removed:
            self.on_remove()
            # TODO: Может Entity не должен взаимодействовать с World?
            self.world.entity_manager.remove_entity(self)
            self._removed = True


class VelocityMixin(BaseEntity):
    """
    Миксин для добавления скорости сущности.
    
    Параметры:
    - max_speed: float - максимальная скорость движения
    - acceleration: float - ускорение при движении
    - friction: float - коэффициент трения (замедление)
    """
    def __init__(self, max_speed: float = 5.0, acceleration: float = 0.5, friction: float = 0.1, **kwargs) -> None:
        super().__init__(**kwargs)
        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.friction = friction
        
    def tick(self) -> None:
        """Обновляет позицию на основе скорости"""
        super().tick()
        self.apply_velocity()
        
    def apply_velocity(self) -> None:
        """Применяет текущую скорость к позиции"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Применяем трение
        self.velocity_x *= (1 - self.friction)
        self.velocity_y *= (1 - self.friction)
        
    def accelerate(self, direction_x: float, direction_y: float) -> None:
        """
        Ускоряет сущность в заданном направлении
        
        Параметры:
        - direction_x, direction_y: float - компоненты вектора направления (-1 до 1)
        """
        self.velocity_x += direction_x * self.acceleration
        self.velocity_y += direction_y * self.acceleration
        
        # Ограничиваем скорость
        speed = (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale


class RepelMixin(VelocityMixin, BaseEntity):
    """
    Миксин для сущностей с отталкиванием при столкновении.
    
    Параметры:
    - repel_force: float - сила отталкивания (0 для полной остановки)
    """
    def __init__(self, repel_force: float = 0.0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.repel_force = repel_force
        
    def on_collision(self, other: BaseEntity) -> None:
        """
        При столкновении:
        - Если repel_force = 0, просто останавливаем движение
        - Иначе отталкиваем обе сущности в противоположные стороны
        """
        if not isinstance(other, RepelMixin):
            return
            
        # Вектор между центрами
        dx = self.x - other.x 
        dy = self.y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance == 0:
            return
            
        # Нормализованный вектор направления
        nx = dx / distance
        ny = dy / distance
        
        if self.repel_force == 0:
            # Просто останавливаем
            self.velocity_x = 0
            self.velocity_y = 0
            other.velocity_x = 0 
            other.velocity_y = 0
        else:
            # Применяем силу отталкивания через ускорение
            self.accelerate(nx * self.repel_force, ny * self.repel_force)
            other.accelerate(-nx * other.repel_force, -ny * other.repel_force)

class DamageMixin(BaseEntity):
    """
    Миксин для сущностей с возможностью наносить урон.
    
    Параметры:
    - damage: int - количество урона, которое сущность может нанести
    """
    def __init__(self, damage: int = 10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.damage = damage


class HealthMixin(BaseEntity):
    """
    Миксин для сущностей с возможностью иметь здоровье.
    
    Параметры:
    - health: int - количество здоровья сущности
    """
    def __init__(self, health: int = 100, **kwargs) -> None:
        super().__init__(**kwargs)
        self.health = health
    
    def damage(self, amount: int) -> None:
        """Наносит урон сущности"""
        self.health -= amount
        if self.health <= 0:
            self.remove()
