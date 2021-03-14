import random

nearby_offsets = [(-1, 0), (0, 1), (1, 0), (0, -1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]


def print_board(board):
    """
    Prints board in 2D format

    board - 2D list of mine locations
    """
    d = len(board)

    for i in range(d):
        print("==", end='')
    print()

    for i in range(d):
        for j in range(d):
            print(board[i][j], end=' ')
        print()

    for i in range(d):
        print("==", end='')
    print()


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


d = 5
board = gen_board(d, 10)
kb = [["?" for i in range(d)] for j in range(d)]
while(True):
    print_board(kb)
    q = (int(input("Query X: ")), int(input("Query Y: ")))
    score = 0

    if(input("Flag as Mine(Y/N): ") == 'Y'):
        if(board[q[0]][q[1]] == 1):
            kb[q[0]][q[1]] = 'M'
            score += 1
        else:
            print("ERROR flagged a clear space")
            break

    if(board[q[0]][q[1]] == 1):
        kb[q[0]][q[1]] = 'M'
    else:
        count = 0
        for i in range(8):
            offset_i, offset_j = nearby_offsets[i]
            pos = (q[0] + offset_i, q[1]+offset_j)

            print(pos)
            if(pos[0] < 0 or pos[0] >= d or pos[1] < 0 or pos[1] >= d):
                continue
            count += board[pos[0]][pos[1]]

        kb[q[0]][q[1]] = count
