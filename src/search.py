from __future__ import annotations
import os
import time
from typing import Optional, Set, Tuple

from src.methods import Method
from src.functions import clear, print_game
from src.sokoban import Board, Direction, Position, State


def successors(board: Board, targets: set[Position], state: State) -> list[State]:
    result = []
    for direction in Direction:
        new_state = state.copy_move(board, direction)
        if new_state is not None and not new_state.is_deadlock(board, targets):
            result.append(new_state)
    return result


def search(method: Method, board: Board, targets: set[Position]) -> tuple[Optional[State], Set, []]:
    explored = set()
    # last = time.time()

    while not method.is_empty():
        state = method.get()

        curr = time.time()
        # if curr - last > 0.1:
        #     clear()
        #     print("Searching solution...")
        #     print_game(board, state)
        #     last = curr

        if state.is_goal(targets):
            return state, explored, method.return_frontier()

        if state not in explored:  # and not state.is_deadlock(board, targets):
            explored.add(state)

            for successor in successors(board, targets, state):
                if successor not in explored:
                    method.add(successor)

    return None, explored, method.return_frontier()


def a_star_search(method: Method, board: Board, targets: set[Position]) -> tuple[Optional[State], Set, []]:
    explored = {}
    #last = time.time()

    while not method.is_empty():
        state = method.get()

        #curr = time.time()
        #if curr - last > 0.1:
        #    clear()
        #    print("Searching solution...")
        #    print_game(board, state)
        #    last = curr

        if state.is_goal(targets):
            return state, explored.values(), method.return_frontier()

        # and not state.is_deadlock(board, targets):
        if state.__hash__() not in explored.keys() or explored[state.__hash__()].cost > state.cost:
            explored[state.__hash__()] = state

            for successor in successors(board, targets, state):
                if successor.__hash__() not in explored.keys() or explored[successor.__hash__()].cost > successor.cost:
                    method.add(successor)

    return None, explored.values(), method.return_frontier()
