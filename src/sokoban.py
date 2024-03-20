from __future__ import annotations
from enum import Enum
from typing import Optional


class Symbol(Enum):
    WALL = '#'
    FREE = ' '
    PLAYER = '@'
    BOX = '$'
    TARGET = '.'
    BOX_ON_TARGET = '*'
    PLAYER_ON_TARGET = '+'


class Tile(Enum):
    WALL = '#'
    FREE = ' '
    TARGET = '·'


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


Position = tuple[int, int]
Matrix = list[list[Symbol]]
Board = list[list[Tile]]


def next_position(position: Position, direction: Direction) -> Position:
    x = position[0] + direction.value[0]
    y = position[1] + direction.value[1]
    return (x, y)


class State:
    def __init__(self, boxes: set[Position], player: Position, history=[]) -> State:
        self.boxes = frozenset(boxes)
        self.player = player
        self.history = history

    def __hash__(self) -> int:
        return hash((self.boxes, self.player))

    def __eq__(self, other: object) -> bool:
        return self.boxes == other.boxes and self.player == other.player

    def can_move(self, board: Board, direction: Direction) -> bool:
        position = next_position(self.player, direction)
        tile = board[position[1]][position[0]]

        if tile == Tile.WALL:
            return False

        if position not in self.boxes:
            return True

        position = next_position(position, direction)
        tile = board[position[1]][position[0]]
        return tile != Tile.WALL and position not in self.boxes

    def copy_move(self, board, direction: Direction) -> Optional[State]:
        if not self.can_move(board, direction):
            return None

        player = next_position(self.player, direction)
        boxes = set(self.boxes)

        if player in self.boxes:
            box = next_position(player, direction)
            boxes.discard(player)
            boxes.add(box)

        new_hist = []
        new_hist += self.history
        new_hist.append(direction)

        return State(boxes, player, new_hist)

    def is_deadlock(self, board, targets) -> bool:
        for box in self.boxes:
            if box not in targets:
                x = box[0]
                y = box[1]
                blockers = {Symbol.WALL, Symbol.BOX, Symbol.BOX_ON_TARGET}
                if (board[y][x + 1] in blockers or board[y][x - 1] in blockers) and (board[y + 1][x] in blockers or board[y - 1][x] in blockers):
                    return True
        return False
