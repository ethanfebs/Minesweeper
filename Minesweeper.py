import random
import copy

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


def print_kb(kb):
    """
    Prints kb in 2D format

    kb - knowledge base of 4 2D arrays
    """
    d = len(kb[0])

    # print upper border
    for i in range(4):
        for j in range(d):
            print("==", end='')
        print(' ', end='')

    print()

    # print 2D list
    for i in range(d):
        for k in range(4):
            for j in range(d):
                print(kb[k][i][j], end=' ')
            print(' ', end='')
        print()

    # print lower border
    for i in range(4):
        for j in range(d):
            print("==", end='')
        print(' ', end='')

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


def init_kb(d: int):
    """
    Generates an empty knowledge base for a board of size d

    kb stores 4 dxd lists of values where
    kb[0] represents the current board state
        kb[0][i][j] = '?' if (i,j) is covered
        kb[0][i][j] = 'M' if (i,j) is an uncovered mine
        if (i,j) is uncovered and safe kb[0][i][j] is the clue value
            for that location, i.e. the number of mines surrounding it

    kb[1] stores the number of safe sqaures identified where
        kb[1][i][j] is the number of safe squares around (i,j)

    kb[2] stores the number of mines identified where
        kb[2][i][j] is the number of mines around (i,j)

    kb[3] stores the number of surrounding hidden squares where
        kb[3][i][j] is the number of hidden squares around (i,j)

    kb - knowledge base of 4 2D arrays
    d - dimension of the board
    """

    # all cells are uncovered to start
    # all cells have no known adjacent safe squares to start
    # all cells have no known adjacenet mines to start
    # every adjacent cell is hidden to start

    kb = [[["?" for i in range(d)] for j in range(d)],
          [[0 for i in range(d)] for j in range(d)],
          [[0 for i in range(d)] for j in range(d)],
          [[8 for i in range(d)] for j in range(d)]]

    # edge cells have only 5 neighbors
    for i in range(d):
        kb[3][0][i] -= 3
        kb[3][i][0] -= 3
        kb[3][d-1][i] -= 3
        kb[3][i][d-1] -= 3

    # corner cells have only 3 neighbors
    kb[3][0][0] += 1
    kb[3][0][d-1] += 1
    kb[3][d-1][0] += 1
    kb[3][d-1][d-1] += 1

    return kb


def num_neighbors(q, d):
    """
    Given a position q, calculate 
    the total number of its neighbors

    q - position on board
    d - dimension of board
    """

    # if q is in a corner, it has 3 neighbors
    if(q == (0, 0) or q == (0, d-1) or q == (d-1, 0) or q == (d-1, d-1)):
        return 3

    # if q is on an edge, it has 5 neighbors
    if(q[0] == 0 or q[0] == d-1 or q[1] == 0 or q[1] == d-1):
        return 5

    # all other positions have 8 neighbors
    return 8


def first_hidden(q, kb):
    """
    Given a position and kb as input
    return location of any hidden location
    surrounding that position

    q - a position on the board
    kb - knowledge base of 4 2D arrays
    """

    d = len(kb[0])

    # iterate over 8 surrounding board locations
    for i in range(len(nearby_offsets)):
        offset_i, offset_j = nearby_offsets[i]
        pos = (q[0] + offset_i, q[1]+offset_j)

        # if pos is out of bounds, continue
        if(pos[0] < 0 or pos[0] >= d or pos[1] < 0 or pos[1] >= d):
            continue

        # when a hidden position is found, return it
        if(kb[0][pos[0]][pos[1]] == '?'):
            return pos

    print("ERROR no hidden locations around"+str(q))

    return (-1, -1)


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


def decide_query_basic(kb):
    """
    Given our knowledge base, decide which location to query next
    and identify if that location should be flagged as a mine

    kb - knowledge base of 4 2D arrays
    """

    flag_mine = False
    d = len(kb[0])

    # iterate over all board spaces to search for basic inferences
    for i in range(d):
        for j in range(d):
            clue = kb[0][i][j]

            # basic inferences can only be made on safe uncovered cells
            if(clue != 'M' and clue != '?'):

                # INFERENCE TYPE 1: If, for a given cell, the total number of mines (the clue)
                # minus the number of revealed mines
                # is the number of hidden neighbors, every hidden neighbor is a mine.

                if((kb[3][i][j] != 0) and (clue - kb[2][i][j]) == kb[3][i][j]):
                    # print("FOUND INFERENCE 1 AT ("+str(i)+", "+str(j)+")")
                    return (first_hidden((i, j), kb), True)

                # INFERENCE TYPE 2: If, for a given cell, the total number of safe neighbors (neighbors - clue)
                # minus the number of revealed safe neighbors
                # is the number of hidden neighbors, every hidden neighbor is safe.

                if((kb[3][i][j] != 0) and (num_neighbors((i, j), d) - clue - kb[1][i][j]) == kb[3][i][j]):
                    # print("FOUND INFERENCE 2 AT ("+str(i)+", "+str(j)+")")
                    return (first_hidden((i, j), kb), False)

    # If no hidden cell can be conclusively identified as a mine or safe,
    # pick a cell to reveal uniformly at random fromthe remaining cells.

    covered = []

    # find every covered location (i,j) on the board
    for i, x in enumerate(kb[0]):
        for j, y in enumerate(x):
            if(y == '?'):
                covered.append((i, j))

    # choose a random covered location to query
    q = random.choice(covered)

    # code for playable game
    # q = (int(input("Query X: ")), int(input("Query Y: ")))
    # if(input("Flag as Mine(Y/N): ") == 'Y'):
    #     flag_mine = True

    return (q, flag_mine)


def update_kb(kb, q, val: chr):
    """
    Given a location and its newly revealed value,
    update the kb appropriately

    kb - knowledge base of 4 2D arrays
    q - position on board that was queried
    val - return value of query
    """

    kb[0][q[0]][q[1]] = val
    d = len(kb[0])

    # iterate over 8 surrounding board locations
    for i in range(len(nearby_offsets)):
        offset_i, offset_j = nearby_offsets[i]
        pos = (q[0] + offset_i, q[1]+offset_j)

        # if pos is out of bounds, continue
        if(pos[0] < 0 or pos[0] >= d or pos[1] < 0 or pos[1] >= d):
            continue

        # if val is not a mine, number of identified safe squares increases by 1
        if(val != 'M'):
            kb[1][pos[0]][pos[1]] += 1
        # if val IS a mine, number of identified mines increases by 1
        else:
            kb[2][pos[0]][pos[1]] += 1

        # number of hidden squares decreases by 1
        kb[3][pos[0]][pos[1]] -= 1

    return kb


def run_game(d, num_mines):
    board = gen_board(d, num_mines)
    kb = init_kb(d)

    score = 0
    revealed = 0

    # loop until all cells have been uncovered
    while(True):
        # print_kb(kb)

        # decide which cell to uncover and whether it should be flagged as a mine
        q, flag_mine = decide_query_basic(kb)

        # agent should never choose to uncover an already uncovered cell
        if(kb[0][q[0]][q[1]] != '?'):
            print("ERROR that location has already been queried")
            continue

        # query at location q and update kb accordingly
        kb = update_kb(kb, q, query(q, board))
        revealed += 1

        if(flag_mine):
            # if a mine is correctly flagged, increment score by 1
            if(kb[0][q[0]][q[1]] == 'M'):
                score += 1
            # agent should never incorrectly flag a cell
            else:
                print("ERROR flagged a clear space")
                break

        # when all cells are uncovered, display score and end game
        if(revealed == d**2):
            # print_board(kb[0])
            # print("Congratulations! Score: "+str(score)+"/"+str(num_mines))
            return score
            break


sum = 0
tests = 100
dim = 25
mines = 150
for i in range(tests):
    sum += run_game(dim, mines)

avg = sum/(tests)
print('Basic Avg(dim='+str(dim)+'): '+str(avg)+'/'+str(mines)+' mines')
