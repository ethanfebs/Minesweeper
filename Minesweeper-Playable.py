import random

nearby_offsets = [(-1, 0), (0, 1), (1, 0), (0, -1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]


def print_board(board):
    """
    Prints board in 2D format

    board - 2D list of mine locations
    """
    d = len(board)

    # print upper border
    for i in range(d):
        print("==", end='')
    print()

    # print 2D list
    for i in range(d):
        for j in range(d):
            print(board[i][j], end=' ')
        print()

    # print lower border
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


def query(q, board):
    """
    Given a position and board as input
    returns 'M' if there is a mine at pos
    and returns the number of surrounding mines otherwise

    q - position on board to query
    board - 2D list of mine locations
    """

    # if a mine exists at q return M
    if(board[q[0]][q[1]] == 1):
        return 'M'

    count = 0
    d = len(board)

    # iterate over 8 surrounding board locations
    for i in range(len(nearby_offsets)):
        offset_i, offset_j = nearby_offsets[i]
        pos = (q[0] + offset_i, q[1]+offset_j)

        # if pos is out of bounds, continue
        if(pos[0] < 0 or pos[0] >= d or pos[1] < 0 or pos[1] >= d):
            continue
        count += board[pos[0]][pos[1]]

    # return number of surrounding mines
    return count


d = 5
board = gen_board(d, 5)
kb = [["?" for i in range(d)] for j in range(d)]
score = 0
revealed = 0

while(True):
    print_board(kb)
    q = (int(input("Query X: ")), int(input("Query Y: ")))

    if(kb[q[0]][q[1]] != '?'):
        print("ERROR that location has already been queried")
        continue

    kb[q[0]][q[1]] = query(q, board)
    revealed += 1

    if(input("Flag as Mine(Y/N): ") == 'Y'):
        if(kb[q[0]][q[1]] == 'M'):
            score += 1
        else:
            print("ERROR flagged a clear space")
            break

    if(revealed == d**2):
        print("Congratulations! Score: "+str(score))
        break
