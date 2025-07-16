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

    decision = 0

    for row in board:
        decision += row.count(X) - row.count(O)

    if decision == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] is EMPTY:
                moves.add((row, column))
    
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)
    row, column = action

    if row < 0 or column < 0:
        raise ValueError("Invalid action: coords must be positive or zero")

    if new_board[row][column] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")
    
    new_board[row][column] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
        
    # Check Columns
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] and board[0][column] is not EMPTY:
            return board[0][column]
    
    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # ASSUME ONLY CALLED WHEN BOARD IS TERMINAL
    w = winner(board)

    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def max_value(board, beta):
        if terminal(board):
            return utility(board)
        
        alpha = -math.inf

        for action in actions(board):
            v = min_value(result(board, action), alpha)

            if v > beta:
                return v

            alpha = max(alpha, v)

        return alpha
    
    def min_value(board, beta):
        if terminal(board):
            return utility(board)
        
        alpha = math.inf

        for action in actions(board):
            v = max_value(result(board, action), alpha)

            if v < beta:
                return v

            alpha = min(alpha, v)

        return alpha

    if terminal(board):
        return None

    current_player = player(board)
    
    value = -math.inf if current_player == X else math.inf 
    selected_action = None

    for action in actions(board):
        action_result = result(board, action)

        if current_player == X:
            v = min_value(action_result, value)
            if value < v:
                value = v
                selected_action = action
        else:
            v = max_value(action_result, value)
            if value > v:
                value = v
                selected_action = action

    return selected_action