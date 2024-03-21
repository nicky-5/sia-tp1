from abc import ABC, abstractmethod

from collections import deque
from heapq import heappop, heappush

from src.heuristics import Heuristic
from src.sokoban import Board, Position, State

class Method(ABC):
    @abstractmethod
    def get(self) -> State:
        pass

    @abstractmethod
    def add(self, state: State):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

class MethodDFS(Method):
    def __init__(self, initial_state: State):
        self.frontier = [initial_state]

    def get(self) -> State:
        return heappop(self.frontier)

    def add(self, state: State):
        heappush(self.frontier, state)

    def is_empty(self) -> bool:
        return len(self.frontier) == 0


class MethodBFS(Method):
    def __init__(self, initial_state: State):
        self.frontier = deque([initial_state])

    def get(self) -> State:
        return self.frontier.popleft()

    def add(self, state: State):
        self.frontier.append(state)

    def is_empty(self) -> bool:
        return len(self.frontier) == 0


class MethodHeuristic(Method):
    def __init__(self, initial_state: State, board: Board, targets: set[Position], heuristic: Heuristic):
        self.board = board
        self.targets = targets
        self.heuristic = heuristic
        self.frontier = [(int(0), initial_state)]

    def get(self) -> State:
        return heappop(self.frontier)[1]

    def add(self, state: State):
        value = self.heuristic(self.board, self.targets, state)
        heappush(self.frontier, (value, state))

    def is_empty(self) -> bool:
        return len(self.frontier) == 0
