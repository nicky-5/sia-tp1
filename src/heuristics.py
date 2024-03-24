from typing import Callable

import numpy as np

from src.sokoban import Board, Position, State, Tile, all_directions
from src.functions import manhattan

Heuristic = Callable[[State], int]


def min_manhattan(targets: set[Position]) -> Heuristic:
    def f(state: State) -> int:
        sum = 0
        for box in state.boxes:
            distances = [manhattan(box, target) for target in targets]
            sum += min(distances)
        return sum
    
    return f


def min_manhattan_modified(targets: set[Position]) -> Heuristic:
    def f(state: State) -> int:
        sum = 0
        from_player = []
        for box in state.boxes:
            distances = [manhattan(box, target) for target in targets]
            sum += min(distances)
            if box not in targets:
                from_player.append(manhattan(box, state.player))
        return sum + min(from_player, default=0) / max(from_player, default=1)
    
    return f


def fast_anti_livelock(heuristic: Heuristic, board: Board) -> Heuristic:
    height = len(board)
    width = len(board[0])
    livelock = np.full(shape=(width, height), fill_value=False, dtype=bool)
    blocked = lambda pos : board[pos[1]][pos[0]] == Tile.WALL

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            (top, bottom, left, right) = all_directions((x, y))
            if (blocked(top) or blocked(bottom)) and (blocked(left) or blocked(right)):
                livelock[x][y] = True

    for x in range(1, width - 1):
        ys = [y for y in range(1, height - 1) if livelock[x][y]]
        if len(ys) == 0:
            continue

        first = min(ys)
        last = max(ys)
        between = range(first + 1, last)

        col_blocked = lambda y : blocked((x - 1, y)) or blocked((x + 1, y))
        col_lock = [col_blocked(y) for y in between]
        if all(col_lock):
            for y in between:
                livelock[x][y] = True

    for y in range(1, height - 1):
        xs = [x for x in range(1, width - 1) if livelock[x][y]]
        if len(xs) == 0:
            continue

        first = min(xs)
        last = max(xs)
        between = range(first + 1, last)

        row_blocked = lambda x : blocked((x, y - 1)) or blocked((x, y + 1))
        row_lock = [row_blocked(x) for x in between]
        if all(row_lock):
            for x in between:
                livelock[x][y] = True
    
    def f(state: State) -> int:
        for box in state.boxes:
            if livelock[box[0]][box[1]]:
                return 1_000_000
            
        return heuristic(state)
    
    return f
