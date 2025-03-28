from tanks.game.base import BaseGame
from tanks.world.world import World

class Game(BaseGame):
    def __init__(self) -> None:
        super().__init__()
        self.world = World()

    def tick(self) -> None:
        super().tick()
        self.world.tick()
