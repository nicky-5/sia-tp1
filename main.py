from src.functions import clear, read_file_to_matrix, game_from_matrix, print_game
from src.methods import MethodDFS, MethodBFS, MethodHeuristic, MethodAStar
from src.heuristics import min_manhattan_modified, min_manhattan, fast_anti_livelock, walkable_distance, anti_wall
from src.search import search, a_star_search
import time
import os

if __name__ == "__main__":
    # Example usage:
    file_name = 'test/test_6'  # Replace 'your_file.txt' with the path to your file
    matrix = read_file_to_matrix(file_name)
    [board, targets, state] = game_from_matrix(matrix)
    print_game(board, state)

    method_heuristic = MethodHeuristic(
        state, fast_anti_livelock(min_manhattan_modified(targets), board))
    # method_heuristic = MethodHeuristic(
    #     state, min_manhattan_modified(targets))

    method_a_star = MethodAStar(state, fast_anti_livelock(
        walkable_distance(board, targets, state), board))
    bfs = MethodBFS(state)
    dfs = MethodDFS(state)

    start = time.time()
    solution, explored, frontier = search(bfs, board, targets)
    # solution, explored, frontier = a_star_search(method_a_star, board, targets)
    end = time.time()

    if solution is None:
        print("No solution found.")
        exit()

    clear()
    # print("Solution found! Replaying in 3 seconds...")
    # time.sleep(3)

    for step, state in enumerate(solution.history(), start=1):
        clear()
        print("Solved in {:.2f} seconds".format(end - start))
        print("Showing move {}".format(step))
        print_game(board, state)
        time.sleep(0.05)
