from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING
from math import sin, cos, pi
from tanks.entity.base import BaseEntity, RepelMixin, VelocityMixin, HealthMixin
from tanks.entity.tank_shell import TankShell

if TYPE_CHECKING:
    from tanks.world.base import BaseWorld


class Tank(VelocityMixin, RepelMixin, HealthMixin, BaseEntity):
    def __init__(self, x: float, y: float, world: BaseWorld, entity_id: UUID | None = None, size: float = 1.0) -> None:
        super().__init__(x=x, y=y, world=world, entity_id=entity_id, size=size,
                         max_speed=3.0, acceleration=0.3, friction=0.1, repel_force=0.5, health=100)
        self.angle: float = 0.0  # Угол поворота танка в радианах
        self.rotation_speed: float = 0.1  # Скорость поворота
        self.left_track: float = 0.0  # Скорость левой гусеницы (-1 до 1)
        self.right_track: float = 0.0  # Скорость правой гусеницы (-1 до 1)
        self.shell_velocity: float = 10.0  # Скорость снаряда
        self.reload_time: int = 60  # Время перезарядки в тиках
        self.reload_timer: int = 0  # Таймер перезарядки

    def set_tracks(self, left: float, right: float) -> None:
        """
        Устанавливает скорость гусениц
        
        Параметры:
        - left: float - скорость левой гусеницы (-1 до 1)
        - right: float - скорость правой гусеницы (-1 до 1)
        """
        self.left_track = max(-1.0, min(1.0, left))
        self.right_track = max(-1.0, min(1.0, right))

    def shoot(self) -> None:
        """Производит выстрел из танка"""
        if self.reload_timer > 0:
            return

        # Создаем снаряд перед танком
        spawn_distance = self.size + 0.5  # Расстояние от центра танка
        shell_x = self.x + cos(self.angle) * spawn_distance
        shell_y = self.y + sin(self.angle) * spawn_distance

        # Создаем и добавляем снаряд в мир
        shell = TankShell(
            x=shell_x,
            y=shell_y,
            angle=self.angle,
            velocity=self.shell_velocity,
            world=self.world,
            creator=self
        )
        self.world.add_entity(shell)

        # Запускаем перезарядку
        self.reload_timer = self.reload_time

    def tick(self) -> None:
        # Обновляем таймер перезарядки
        if self.reload_timer > 0:
            self.reload_timer -= 1

        # Вычисляем поворот на основе разницы скоростей гусениц
        rotation = (self.right_track - self.left_track) * self.rotation_speed
        self.angle = (self.angle + rotation) % (2 * pi)

        # Вычисляем движение вперед на основе средней скорости гусениц
        forward_speed = (self.left_track + self.right_track) / 2.0

        # Преобразуем в векторы направления
        direction_x = cos(self.angle) * forward_speed
        direction_y = sin(self.angle) * forward_speed

        # Применяем ускорение в нужном направлении
        self.accelerate(direction_x, direction_y)

        super().tick()
