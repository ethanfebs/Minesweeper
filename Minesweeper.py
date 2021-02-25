import random


def gen_board(d: int, n: int):
    """
    Generates a d x d square board with randomly placed mines

    d - dimension of the board
    n - number of mines
    """

    # select n integers from the set {0 ... d*d}
    mines = random.sample(range(d*d), n)
    # create d x d nested list with values preset to 0
    board = [[0 for i in range(d)] for j in range(d)]

    for mine in mines:
        # for each mine location set corresponding board location to 1
        board[mine // d][mine % d] = 1

    return board


board = gen_board(3, 3)
print(board)
