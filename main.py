from src.sokoban import Direction
from src.functions import read_file_to_matrix, game_from_matrix, print_game
from src.search import Game, BFS, DFS
import time
import os

if __name__ == "__main__":

    # print_game(board, state)
    # print(targets)

    # list = []
    # for direction in Direction:
    #     list.append(state.copy_move(board, direction))

    # for e in list:
    #     if e is not None:
    #         print_game(board, e)

    # Example usage:
    file_name = 'test/test_4'  # Replace 'your_file.txt' with the path to your file
    matrix = read_file_to_matrix(file_name)
    [board, targets, state] = game_from_matrix(matrix)

    game = Game(board, targets)

    bfs = BFS(initial_state=state, game=game)
    solution = bfs.search()
    # dfs = DFS(initial_state=state, game=game)
    # solution = dfs.search()

    print(solution)
    if solution:
        print("Solution found:", solution)
    else:
        print("No solution found.")

    print(solution.history)

    os.system('cls' if os.name == 'nt' else 'clear')

    cur_state = state
    print_game(board, cur_state)
    for d in solution.history:
        time.sleep(0.01)
        os.system('cls' if os.name == 'nt' else 'clear')
        cur_state = cur_state.copy_move(board, d)
        print_game(board, cur_state)
