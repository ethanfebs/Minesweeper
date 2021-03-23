from Minesweeper import run_game as basic_algorithm, gen_board, print_board
from Minesweeper_Advanced import run_game as advanced_algorithm

if __name__ == "__main__":
    dim = 10
    mines = 40
    board = gen_board(dim, mines)
    # board = [[0, 0, 0, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [1, 0, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 1, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 1, 0,], [0, 1, 1, 0, 0, 1, 1, 0, 1, 0], [1, 0, 0, 1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 1, 0, 0, 0, 0]]
    # for i in range(len(board)):
    #     print(len(board[i]))
    # basic_score = basic_algorithm(dim, mines, board, True)
    advanced_score = advanced_algorithm(dim, mines, board, True)
    print_board(board)
    print(advanced_score)
