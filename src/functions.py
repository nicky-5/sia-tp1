from src.sokoban import Symbol, Tile, State, Matrix, Board


def read_file_to_matrix(file_name: str) -> Matrix:
    with open(file_name, 'r') as file:
        return [list(map(Symbol, line.strip('\n'))) for line in file]


def match_symbol(symbol: Symbol) -> Tile:
    match symbol:
        case Symbol.WALL:
            return Tile.WALL
        case Symbol.FREE | Symbol.PLAYER | Symbol.BOX:
            return Tile.FREE
        case Symbol.TARGET | Symbol.BOX_ON_TARGET | Symbol.PLAYER_ON_TARGET:
            return Tile.TARGET


def game_from_matrix(matrix: Matrix) -> tuple[Board, State]:
    board = [list(map(match_symbol, row)) for row in matrix]

    boxes = set()
    player = tuple()
    targets = set()
    for y, row in enumerate(matrix):
        for x, symbol in enumerate(row):
            match symbol:
                case Symbol.PLAYER:
                    player = (x, y)
                case Symbol.BOX:
                    boxes.add((x, y))
                case Symbol.TARGET:
                    targets.add((x, y))
                case Symbol.BOX_ON_TARGET:
                    boxes.add((x, y))
                    targets.add((x, y))
                case Symbol.PLAYER_ON_TARGET:
                    player = (x, y)
                    targets.add((x, y))

    return (board, targets, State(boxes, player))


def print_game(board: Board, state: State):
    mapped = [list(map(lambda s: s.value, row)) for row in board]
    for box in state.boxes:
        if board[box[1]][box[0]] == Tile.TARGET:
            mapped[box[1]][box[0]] = Symbol.BOX_ON_TARGET.value
        else:
            mapped[box[1]][box[0]] = Symbol.BOX.value

    player = state.player
    if board[player[1]][player[0]] == Tile.TARGET:
        mapped[player[1]][player[0]] = Symbol.PLAYER_ON_TARGET.value
    else:
        mapped[player[1]][player[0]] = Symbol.PLAYER.value

    for row in mapped:
        # Join the characters in the row into a single string
        row_str = ''.join(row)
        print(row_str)
