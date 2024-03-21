from typing import Callable

from src.sokoban import Board, Position, State
from src.functions import manhattan

Heuristic = Callable[[Board, set[Position], State], int]


def min_manhattan(_: Board, targets: set[Position], state: State) -> int:
    sum = 0
    for box in state.boxes:
        distances = [manhattan(box, target) for target in targets]
        sum += min(distances)

    return sum


def min_manhattan_modified(_: Board, targets: set[Position], state: State) -> int:
    sum = 0
    from_player = []
    for box in state.boxes:
        distances = [manhattan(box, target) for target in targets]
        sum += min(distances)
        if box not in targets:
            from_player.append(manhattan(box, state.player))

    return sum + min(from_player, default=0) / max(from_player, default=1)
