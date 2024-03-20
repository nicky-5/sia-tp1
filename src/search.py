from collections import deque
from src.functions import print_game
from src.sokoban import Direction
import bisect


class DFS_method():
    def init(self, initial_state):
        self.frontier = [initial_state]

    def get(self):
        return self.frontier.pop()

    def add(self, state):
        self.frontier.append(state)

    def is_empty(self):
        return len(self.frontier) == 0


class BFS_method():
    def init(self, initial_state):
        self.frontier = deque([initial_state])
        return self

    def get(self):
        return self.frontier.popleft()

    def add(self, state):
        self.frontier.append(state)

    def is_empty(self):
        return len(self.frontier) == 0


class OrderedCustomList:
    def __init__(self, comparator=None):
        self._data = []
        self._comparator = comparator or (lambda x: x)

    def add(self, item):
        bisect.insort(self._data, item, key=self._comparator)

    def is_empty(self):
        return len(self._data) == 0

    def pop(self):
        return self._data.pop()

    def __repr__(self):
        return repr(self._data)


# Example of a comparator function
def custom_comparator(item):
    return item[1]  # Sorting based on the second element of a tuple


class Heuristic_1:
    def __init__(self, targets):
        self.targets = targets

    def calculate_prediction(self, state):
        target = 0
        for tar in self.targets:
            target = tar
            break
        sum = 0
        for box in state.boxes:
            sum -= abs(box[0] - target[0]) + abs(box[1] - target[1])
            # sum -= abs(state.player[0] - box[0]) + abs(state.player[1] - box[1])
        return sum


class Heuristic_2:
    def __init__(self, targets):
        self.targets = targets

    def calculate_prediction(self, state):
        sum = 0
        for target in self.targets:
            for box in state.boxes:
                sum -= abs(box[0] - target[0]) + abs(box[1] - target[1])
        return sum


class HeuristicMethod:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def init(self, initial_state):
        self.frontier = OrderedCustomList(custom_comparator)
        self.add(initial_state)
        return self

    def get(self):
        return self.frontier.pop()[0]

    def add(self, state):
        value = self.heuristic.calculate_prediction(state)
        item = (state, value)
        self.frontier.add(item)

    def is_empty(self):
        return self.frontier.is_empty()


class Search:
    def __init__(self, initial_state, game, method):
        self.initial_state = initial_state
        self.game = game
        self.method = method

    def search(self):
        # frontier = deque([Node(self.initial_state)])
        self.method.init(self.initial_state)
        explored = set()

        while not self.method.is_empty():
            # current_node = frontier.popleft()
            # current_state = current_node.state
            current_state = self.method.get()

            if self.game.goal_test(current_state):
                return current_state

            if current_state not in explored and not current_state.is_deadlock(self.game.board, self.game.targets):
                explored.add(current_state)

                for successor_state in self.game.successors(current_state):
                    # and not self._is_in_frontier(frontier, successor_state):
                    if successor_state not in explored:
                        self.method.add(successor_state)

        return None


class Game:
    def __init__(self, board, targets):
        self.board = board
        self.targets = targets

    def goal_test(self, state):
        for box in state.boxes:
            if box not in self.targets:
                return False
        return True

    def successors(self, state):
        result = []
        for direction in Direction:
            new_state = state.copy_move(self.board, direction)
            if new_state is not None:
                #     if not new_state.is_deadlock(self.board, self.targets):
                #         result.append(new_state)
                result.append(new_state)
        return result
