from __future__ import annotations
from collections import deque
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


def all_directions(position: Position) -> tuple[Position]:
    top = next_position(position, Direction.UP)
    bottom = next_position(position, Direction.DOWN)
    left = next_position(position, Direction.LEFT)
    right = next_position(position, Direction.RIGHT)
    return (top, bottom, left, right)


class State:
    def __init__(self, boxes: set[Position], player: Position, past: State | None = None):
        self.boxes = frozenset(boxes)
        self.player = player
        self.past = past
        if past is None:
            self.cost = 0
        else:
            self.cost = past.cost + 1

    def __hash__(self) -> int:
        return hash((self.boxes, self.player))

    def __eq__(self, other: State) -> bool:
        return other != None and self.boxes == other.boxes and self.player == other.player

    def __lt__(self, _: State) -> bool:
        return False

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
            boxes.remove(player)
            boxes.add(box)

        return State(boxes, player, self)

    def history(self) -> list[State]:
        hist = deque([self])
        state = self
        while state.past != None:
            hist.appendleft(state.past)
            state = state.past

        return list(hist)

    def is_deadlock(self, board: Board, targets: set[Position]) -> bool:
        for box in self.boxes:
            if box in targets:
                continue

            (top, bottom, left, right) = all_directions(box)

            def occupied(pos): return board[pos[1]][pos[0]] == Tile.WALL
            if (occupied(top) or occupied(bottom)) and (occupied(left) or occupied(right)):
                return True

            def occupied_box(pos): return occupied(pos) or pos in self.boxes
            if (occupied_box(top) or occupied_box(bottom)) and (occupied_box(left) or occupied_box(right)):
                other_box = [pos for pos in [top, bottom, left, right] if pos in self.boxes][0]

                (other_top, other_bottom, other_left,
                 other_right) = all_directions(other_box)

                if (occupied_box(other_top) or occupied_box(other_bottom)) and (occupied_box(other_left) or occupied_box(other_right)):
                    return True

        return False

    def is_goal(self, targets: set[Position]) -> bool:
        return self.boxes.issubset(targets)
