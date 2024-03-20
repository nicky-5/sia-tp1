from collections import deque
from src.functions import print_game
from src.sokoban import Direction


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent


class BFS:
    def __init__(self, initial_state, game):
        self.initial_state = initial_state
        self.game = game

    def search(self):
        # frontier = deque([Node(self.initial_state)])
        frontier = deque([self.initial_state])
        explored = set()

        while frontier:
            # current_node = frontier.popleft()
            # current_state = current_node.state
            current_state = frontier.popleft()

            if self.game.goal_test(current_state):
                return current_state

            if current_state not in explored and not current_state.is_deadlock(self.game.board, self.game.targets):
                explored.add(current_state)

                for successor_state in self.game.successors(current_state):
                    # and not self._is_in_frontier(frontier, successor_state):
                    if successor_state not in explored:
                        frontier.append(successor_state)

        return None

    def _get_solution(self, node):
        solution = []
        while node:
            solution.append(node.state)
            node = node.parent
        return list(reversed(solution))

    def _is_in_frontier(self, frontier, state):
        return any(node.state == state for node in frontier)


class DFS:
    def __init__(self, initial_state, game):
        self.initial_state = initial_state
        self.game = game

    def search(self):
        # frontier = deque([Node(self.initial_state)])
        frontier = [self.initial_state]
        explored = set()

        while frontier:
            # current_node = frontier.popleft()
            # current_state = current_node.state
            current_state = frontier.pop()

            if self.game.goal_test(current_state):
                return current_state

            if current_state not in explored and not current_state.is_deadlock(self.game.board, self.game.targets):
                explored.add(current_state)

                for successor_state in self.game.successors(current_state):
                    # and not self._is_in_frontier(frontier, successor_state):
                    if successor_state not in explored:
                        frontier.append(successor_state)

        return None

    def _get_solution(self, node):
        solution = []
        while node:
            solution.append(node.state)
            node = node.parent
        return list(reversed(solution))

    def _is_in_frontier(self, frontier, state):
        return any(node.state == state for node in frontier)


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
