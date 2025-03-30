from __future__ import annotations

from math import atan2, pi, cos, sin
from typing import TYPE_CHECKING
from tanks.entity.tank import Tank

if TYPE_CHECKING:
    from tanks.world.base import BaseWorld


class TankBot(Tank):
    def __init__(self, x: float, y: float, world: BaseWorld) -> None:
        super().__init__(x=x, y=y, world=world)
        self.target: Tank | None = None
        self.attack_range = 20.0  # Дистанция атаки
        self.rotation_speed = 0.1  # Скорость поворота
        self.update_target_interval = 10  # Частота обновления цели
        self.ticks_since_target_update = 0

    def find_nearest_player(self) -> Tank | None:
        """Находит ближайшего игрока-танк"""
        nearest_distance = float('inf')
        nearest_tank = None

        for entity in self.world.entity_manager.entities.values():
            if isinstance(entity, Tank) and entity != self:
                dx = entity.x - self.x
                dy = entity.y - self.y
                distance = (dx * dx + dy * dy) ** 0.5

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_tank = entity

        return nearest_tank

    def get_angle_to_target(self) -> float:
        """Вычисляет угол до цели"""
        if not self.target:
            return 0.0

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        return atan2(dy, dx)

    def rotate_to_target(self) -> None:
        """Поворачивает танк к цели"""
        if not self.target:
            return

        target_angle = self.get_angle_to_target()
        angle_diff = target_angle - self.angle

        # Нормализуем разницу углов в диапазон [-pi, pi]
        while angle_diff > pi:
            angle_diff -= 2 * pi
        while angle_diff < -pi:
            angle_diff += 2 * pi

        # Поворачиваем в сторону цели
        if abs(angle_diff) > self.rotation_speed:
            if angle_diff > 0:
                self.angle += self.rotation_speed
            else:
                self.angle -= self.rotation_speed

    def get_distance_to_target(self) -> float:
        """Вычисляет расстояние до цели"""
        if not self.target:
            return float('inf')

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        return (dx * dx + dy * dy) ** 0.5

    def tick(self) -> None:
        # Периодически обновляем цель
        self.ticks_since_target_update += 1
        if self.ticks_since_target_update >= self.update_target_interval:
            self.target = self.find_nearest_player()
            self.ticks_since_target_update = 0

        if self.target:
            # Поворачиваемся к цели
            self.rotate_to_target()

            distance = self.get_distance_to_target()

            # Если цель далеко - движемся к ней
            if distance > self.attack_range:
                # Устанавливаем одинаковую скорость для обеих гусениц чтобы ехать прямо
                self.set_tracks(left=1.0, right=1.0)

            # Если цель в зоне атаки и мы повернуты к ней - стреляем
            elif abs(self.get_angle_to_target() - self.angle) < 0.1:
                self.shoot()

        super().tick()
