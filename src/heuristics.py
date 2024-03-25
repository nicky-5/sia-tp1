import numpy as np
import sys
from typing import Callable, Dict, Tuple
from src.sokoban import Board, Position, State, Tile, all_directions, Symbol
from src.functions import manhattan

Heuristic = Callable[[State], int]

# Heuristic = Callable[[Board, set[Position], State], int]


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
    def blocked(pos): return board[pos[1]][pos[0]] == Tile.WALL

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            (top, bottom, left, right) = all_directions((x, y))
            if (blocked(top) or blocked(bottom)) and (blocked(left) or blocked(right)) and board[y][x] != Tile.TARGET:
                livelock[x][y] = True

    for x in range(1, width - 1):
        ys = [y for y in range(1, height - 1) if livelock[x][y]]
        if len(ys) == 0:
            continue

        first = min(ys)
        last = max(ys)
        between = range(first + 1, last)

        def col_blocked(y): return (blocked((x - 1, y))
                                    or blocked((x + 1, y))) and board[y][x] != Tile.TARGET
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

        def row_blocked(x): return (blocked((x, y - 1))
                                    or blocked((x, y + 1))) and board[y][x] != Tile.TARGET
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
    # return sum + min(from_player, default=0) / max(from_player, default=1)    # TODO: Que es esto?


distance_point_to_point: Dict[Tuple[Tuple[int,
                                          int], Tuple[int, int]], int] = {}


def walkable_distance(_: Board, targets: set[Position], state: State) -> Heuristic:
    def f(state: State) -> int:
        closest_box = sys.maxsize

        for box in state.boxes:
            if (box in targets):
                continue
            if ((box, state.player) in distance_point_to_point):
                distance = distance_point_to_point[(box, state.player)]
            else:
                distance = walkable_distance_helper(_, state.player, box)
                distance_point_to_point[(box, state.player)] = distance
                distance_point_to_point[(state.player, box)] = distance
            if distance < closest_box:
                closest_box = distance
        sum = 0

        for box in state.boxes:
            closest_box_target = sys.maxsize
            for target in targets:
                if ((box, target) in distance_point_to_point):
                    distance = distance_point_to_point[(box, target)]
                else:
                    distance = walkable_distance_helper(_, box, target)
                    distance_point_to_point[(box, target)] = distance
                    distance_point_to_point[(target, box)] = distance

                if distance < closest_box_target:
                    closest_box_target = distance
            sum += closest_box_target

        return closest_box + sum
    return f


def walkable_distance_helper(board: Board, point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    queue = []
    queue.append((point1, 0))
    explored = set()

    while queue:
        point1, distance = queue.pop(0)
        if point1 in explored:
            continue
        explored.add(point1)

        if point1 == point2:
            return distance

        for cordx, cordy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if board[point1[1] + cordy][point1[0] + cordx].value != Symbol.WALL.value:
                queue.append(
                    ((point1[0] + cordx, point1[1] + cordy), distance + 1))

    return sys.maxsize


def inadmissible_manhattan_distance(_: Board, targets: set[Position], state: State) -> Heuristic:
    def f(state: State) -> int:
        x, y = state.player()

        playerToBoxes = 0

        for e in state.boxes():
            bx, by = e
            playerToBoxes += abs(x - bx) + abs(y - by)

        boxesToStorages = 0

        for e in targets:
            ex, ey = e

            minDistance = 0

            for m in state.boxes():
                mx, my = m
                distance = abs(ex - mx) + abs(ey - my)
                minDistance = min(minDistance, distance)

            boxesToStorages += minDistance

        return playerToBoxes + boxesToStorages
    return f


def manhattan_mod(_: Board, targets: set[Position], state: State) -> Heuristic:
    def f(state: State) -> int:
        distance_player_closet_box = sys.maxsize
        player = state.player

        for box in state.boxes:
            distance = abs(player[1] - box[1]) + abs(player[0] - box[0])
            if distance < distance_player_closet_box:
                distance_player_closet_box = distance

        sum_distance_boxes_goals = 0

        for box in state.boxes:
            distance_box_closest_goal = sys.maxsize

            for target in targets:
                distance = abs(box[1] - target[1]) + abs(box[0] - target[0])
                if distance < distance_box_closest_goal:
                    distance_box_closest_goal = distance

            sum_distance_boxes_goals += distance_box_closest_goal

        return distance_player_closet_box + sum_distance_boxes_goals
    return f
