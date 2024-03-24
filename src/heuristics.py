from typing import Callable,Dict,Tuple
import sys
from src.sokoban import Board, Position, State, Symbol
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


distance_point_to_point: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}

def walkable_distance(_: Board, targets: set[Position], state: State) -> int:
    closest_box = sys.maxsize

    for box in state.boxes:
        if(box in targets):
            continue
        if((box,state.player) in distance_point_to_point):
                distance = distance_point_to_point[(box,state.player)]
        else:
            distance = walkable_distance_helper(_,state.player,box)
            distance_point_to_point[(box,state.player)] = distance
            distance_point_to_point[(state.player,box)] = distance
        if distance < closest_box:
            closest_box = distance
    sum = 0

    for box in state.boxes:
        closest_box_target = sys.maxsize
        for target in targets:
            if((box,target) in distance_point_to_point):
                distance = distance_point_to_point[(box,target)]
            else:
                distance = walkable_distance_helper(_,box,target)
                distance_point_to_point[(box,target)] = distance
                distance_point_to_point[(target,box)] = distance
            
            if distance < closest_box_target:
                closest_box_target = distance
        sum += closest_box_target
                   

    return closest_box + sum

def walkable_distance_helper(board: Board, point1: Tuple[int,int], point2: Tuple[int,int]) -> int:
    queue = []
    queue.append((point1,0))
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
                queue.append(( (point1[0] + cordx,point1[1] + cordy), distance + 1 ))

    return sys.maxsize

def inadmissible_manhattan_distance(sokoban: Sokoban) -> int:
    x, y = sokoban.get_player()

    playerToBoxes = 0

    for e in sokoban.get_boxes():
        bx, by = e
        playerToBoxes += abs(x - bx) + abs(y - by)

    boxesToStorages = 0

    for e in sokoban.get_goals():
        ex, ey = e

        minDistance = 0

        for m in sokoban.get_boxes():
            mx, my = m
            distance = abs(ex - mx) + abs(ey - my)
            minDistance = min(minDistance, distance)

        boxesToStorages += minDistance

    return playerToBoxes + boxesToStorages

def manhattan_mod(_:Board, targets: set[Position], state: State) -> int:
        distance_player_closet_box= sys.maxsize
        player = state.player

        for box in state.boxes:
            distance = abs(player[1] - box[1]) + abs(player[0] - box[0])
            if distance < distance_player_closet_box:
                distance_player_closet_box = distance
        
        sum_distance_boxes_goals = 0

        for box in state.boxes:
            distance_box_closest_goal = sys.maxsize
            
            for target in targets:
                distance = abs(box[1] - target[1]) + abs(box[0] -target[0])
                if distance < distance_box_closest_goal:
                    distance_box_closest_goal = distance

            sum_distance_boxes_goals += distance_box_closest_goal

        return distance_player_closet_box + sum_distance_boxes_goals    