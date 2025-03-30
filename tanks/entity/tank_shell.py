from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING
from math import sin, cos
from tanks.entity.base import BaseEntity, VelocityMixin, DamageMixin, HealthMixin

if TYPE_CHECKING:
    from tanks.world.base import BaseWorld
    from tanks.entity.tank import Tank

class TankShell(VelocityMixin, DamageMixin, BaseEntity):
    def __init__(
        self, 
        x: float, 
        y: float, 
        angle: float,
        velocity: float,
        world: BaseWorld,
        creator: Tank,
        entity_id: UUID | None = None,
        size: float = 0.2
    ) -> None:
        super().__init__(
            x=x,
            y=y, 
            world=world,
            entity_id=entity_id,
            size=size,
            max_speed=velocity,
            acceleration=0,
            friction=0,
            damage=10
        )
        
        self.creator = creator
        
        # Задаем начальную скорость снаряда
        self.velocity_x = cos(angle) * velocity
        self.velocity_y = sin(angle) * velocity

    def tick(self) -> None:
        # Снаряд движется прямолинейно с постоянной скоростью
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        super().tick()
        
    def on_collision(self, other: BaseEntity) -> None:
        if other == self.creator:
            return

        if isinstance(other, HealthMixin):
            other.damage(self.damage)
            self.remove()
        else:
            self.remove()

    def on_world_boundary(self) -> None:
        self.remove()
