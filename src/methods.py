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

    @abstractmethod
    def return_frontier(self) -> []:
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

    def return_frontier(self) -> []:
        return self.frontier


class MethodBFS(Method):
    def __init__(self, initial_state: State):
        self.frontier = deque([initial_state])

    def get(self) -> State:
        return self.frontier.popleft()

    def add(self, state: State):
        self.frontier.append(state)

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def return_frontier(self) -> []:
        return self.frontier


class MethodHeuristic(Method):
    def __init__(self, initial_state: State, heuristic: Heuristic):
        self.heuristic = heuristic
        self.frontier = [(int(0), initial_state)]

    def get(self) -> State:
        return heappop(self.frontier)[1]

    def add(self, state: State):
        value = self.heuristic(state)
        heappush(self.frontier, (value, state))

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def return_frontier(self) -> []:
        second_values = [tup[1] for tup in self.frontier]
        return second_values


class MethodAStar(Method):
    def __init__(self, initial_state: State, heuristic: Heuristic):
        self.heuristic = heuristic
        self.frontier = [(int(0), initial_state)]

    def get(self) -> State:
        return heappop(self.frontier)[1]

    def add(self, state: State):
        value = self.heuristic(state) + state.cost
        heappush(self.frontier, (value, state))

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def return_frontier(self) -> []:
        second_values = [tup[1] for tup in self.frontier]
        return second_values
