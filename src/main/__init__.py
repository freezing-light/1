"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple, Optional


class Facing(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}

    @property
    def current_pos(self) -> Tuple[int, int]:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:

        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError("Position must be a tuple of length 2")

        x, y = value
        x = int(x)
        y = int(y)

        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))

        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:

        x, y = self.current_pos

        if self.current_direction == Facing.RIGHT:
            new_pos = (x + 1, y)
        elif self.current_direction == Facing.UP:
            new_pos = (x, y + 1)
        elif self.current_direction == Facing.LEFT:
            new_pos = (x - 1, y)
        elif self.current_direction == Facing.DOWN:
            new_pos = (x, y - 1)
        else:
            new_pos = (x, y)

        self.current_pos = new_pos
        return new_pos

    def turn_left(self) -> Facing:

        current_value = self.current_direction.value
        new_value = (current_value + 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def turn_right(self) -> Facing:

        current_value = self.current_direction.value
        new_value = (current_value - 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def find_enemy(self) -> bool:

        return self.current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:

        self.position_history[step] = self.current_pos

    def get_position_at_step(self, step: int) -> Optional[tuple]:

        return self.position_history.get(step, None)


class AdvancedGrid(Grid):

    def __init__(self, width: int, height: int, enemy_pos: tuple):
        super().__init__(width, height, enemy_pos)
        self.steps: int = 0

    def move_forward(self) -> Tuple[int, int]:

        new_pos = super().move_forward()
        self.steps += 1
        return new_pos

    def distance_to_enemy(self) -> int:

        x1, y1 = self.current_pos
        x2, y2 = self.enemy_pos
        return abs(x1 - x2) + abs(y1 - y2)
