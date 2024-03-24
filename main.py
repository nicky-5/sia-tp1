from src.functions import clear, read_file_to_matrix, game_from_matrix, print_game
from src.methods import MethodDFS, MethodBFS, MethodHeuristic, MethodAStar
from src.heuristics import min_manhattan_modified, min_manhattan, walkable_distance
from src.search import search, a_star_search
import time
import os

if __name__ == "__main__":
    # Example usage:
    file_name = 'test/test_2'  # Replace 'your_file.txt' with the path to your file
    matrix = read_file_to_matrix(file_name)
    [board, targets, state] = game_from_matrix(matrix)
    print_game(board, state)

    heuristic = MethodHeuristic(state, board, targets, min_manhattan_modified)
    method_a_star = MethodAStar(state, board, targets, min_manhattan_modified)
    bfs = MethodBFS(state)
    dfs = MethodDFS(state)

    start = time.time()
    solution = search(bfs, board, targets)
    #solution = a_star_search(method_a_star, board, targets)
    end = time.time()

    if solution is None:
        print("No solution found.")
        exit()

    clear()
    print("Solution found! Replaying in 3 seconds...")
    time.sleep(3)

    for state in solution.history():
        clear()
        print("Solved in {:.2f} seconds".format(end - start))
        print_game(board, state)
        time.sleep(0.05)
