from enum import Enum


class Box:
    def __init__(self, position):
        self.x = position[1]
        self.y = position[0]

    def can_move(self, board, boxes, direction):
        x_new = self.x + direction.value[0]
        y_new = self.y + direction.value[1]
        x_op = self.x - direction.value[0]
        y_op = self.y - direction.value[1]
        new = board[y_new][x_new]
        opposite = board[y_op][x_op]
        if opposite == Symbols.WALL.value or new == Symbols.WALL.value:
            return False
        else:
            for box in boxes:
                if (x_op == box.x and y_op == box.y) or (x_new == box.x and y_new == box.y):
                    return False
        return True

    def move(self, board, boxes, direction):
        if self.can_move(board, boxes, direction):
            self.x += direction.value

    def get_position(self):
        return self.x, self.y


class Player:
    def __init__(self, position):
        self.x, self.y = position

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_position(self):
        return self.x, self.y


def find_all_symbols(matrix, symbol):
    positions = []
    for row_index, row in enumerate(matrix):
        for col_index, char in enumerate(row):
            if char == symbol:
                positions.append((row_index, col_index))
    return positions


class Symbols(Enum):
    WALL = '#'
    EMPTY = ' '
    PLAYER = '@'
    BOX = '$'
    TARGET = '.'
    BOX_ON_TARGET = '*'


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def read_file_to_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        for line in file:
            # Strip the newline character and split the line into characters
            row = list(line.strip('\n'))
            # Replace spaces with '0'
            matrix.append(row)
    return matrix


def print_matrix(matrix):
    for row in matrix:
        # Join the characters in the row into a single string
        row_str = ''.join(row)
        print(row_str)


if __name__ == "__main__":

    # Example usage:
    file_name = 'test/test1'  # Replace 'your_file.txt' with the path to your file
    matrix = read_file_to_matrix(file_name)
    player_position = find_all_symbols(matrix, Symbols.PLAYER.value)[0]
    boxes_positions = find_all_symbols(matrix, Symbols.BOX.value)
    boxes_on_target = find_all_symbols(matrix, Symbols.BOX_ON_TARGET.value)
    target = find_all_symbols(matrix, Symbols.TARGET.value)

    board = matrix

    player = Player(player_position)
    board[player.x][player.y] = ' '

    boxes = []
    for box_p in boxes_positions:
        box = Box(box_p)
        boxes.append(box)
        board[box.y][box.x] = ' '

    for pos in boxes_on_target:
        box = Box(pos)
        boxes.append(box)
        board[box.y][box.y] = ' '
    print_matrix(board)
    print(boxes[0].can_move(board, boxes, Direction.RIGHT))
