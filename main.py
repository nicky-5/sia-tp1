from src.sokoban import *
from src.functions import *

if __name__ == "__main__":

    # Example usage:
    file_name = 'test/test1'  # Replace 'your_file.txt' with the path to your file
    matrix = read_file_to_matrix(file_name)
    [board, state] = game_from_matrix(matrix)

    print_game(board, state)
