"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    num_x = 0
    for row in board:
        for val in row:
            if val == X:
                num_x += 1
    if (num_x % 2 == 0): 
        return X
    return O 



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    for i,row in enumerate(board):
        for j,val in enumerate(row):
            if val == EMPTY: actions.add((i, j))

    return actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if type(action) != 'tuple'  or type(action[1]) != 'int' or type(action[0] != 'int'):
        raise TypeError("tuple of ints")
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise IndexError("Index value out of bounds")
    
    temp = copy.deepcopy(board)
    player = player(board)
    temp[action[0]][action[1]] = player
    return temp
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for player in [X, O]:
        if (any(all(board[i][j] == player for j in range(3)) for i in range(3)) or # check horizontal
            any(all(board[i][j] == player for i in range(3)) for j in range(3)) or # check vertically
            (board[1][1] == player and ((board[0][0] == player and board[2][2] == player) or (board[0][2] == player and board[2][0] == player)))):
            return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if ( winner(board) is not None or
        len(actions(board) == 0)):
        return True
    return False 



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if terminal(board) and win:
        return 1 if win == X else -1
    return 0
    


    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
