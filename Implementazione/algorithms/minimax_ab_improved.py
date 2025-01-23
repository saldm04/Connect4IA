"""
Implementazione di Minimax con potatura alpha-beta e decisione imperfette in tempo reale.
(Profondità massima e funzione di valutazione euristica)
L'algoritmo esplora l'intero game tree e restituisce:
  - -1 se lo stato è vincente per il giocatore umano (PLAYER_PIECE),
  - +1 se lo stato è vincente per l'IA (AI_PIECE),
  - 0 se lo stato rappresenta un pareggio.
"""
from board import (
    PLAYER_PIECE,
    AI_PIECE,
    winning_move,
    get_valid_locations,
    get_next_open_row,
    drop_piece,
    is_terminal_node,
    score_position,
    ROWS,
    COLS
)

def is_draw(board):
    """
    Restituisce True se la board non ha mosse valide (pareggio).
    """
    return len(get_valid_locations(board)) == 0


def clone_board(board):
    """
    Crea e restituisce una copia della board.
    """
    return board.copy()


def minimax_alpha_beta(board, maximizing_player, alpha, beta, depth, max_depth):
    # Controllo dei casi terminali
    if winning_move(board, PLAYER_PIECE):
        return -10000
    if winning_move(board, AI_PIECE):
        return +10000
    if is_draw(board):
        return 0

    if depth == max_depth:
        return score_position(board, AI_PIECE)  # Sempre dal punto di vista dell’IA

    valid_locations = get_valid_locations(board)

    if maximizing_player:
        best_value = float('-inf')
        for col in valid_locations:
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, AI_PIECE)
            value = minimax_alpha_beta(new_board, False, alpha, beta, depth + 1, max_depth)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        return best_value
    else:
        best_value = float('inf')
        for col in valid_locations:
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, PLAYER_PIECE)
            value = minimax_alpha_beta(new_board, True, alpha, beta, depth + 1, max_depth)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if alpha >= beta:
                break
        return best_value



def find_best_move(board, max_depth):
    """
    Determina la migliore mossa per l'IA (AI_PIECE) in base allo stato corrente della board,
    valutando le possibili mosse tramite l'algoritmo minimax con potatura alpha-beta
    e un limite di profondità parametrizzato.
    """

    best_value = float('-inf')
    best_col = None

    for col in get_valid_locations(board):
        new_board = clone_board(board)
        row = get_next_open_row(new_board, col)
        drop_piece(new_board, row, col, AI_PIECE)
        move_value = minimax_alpha_beta(new_board, False, float('-inf'), float('inf'), 1, max_depth)
        if move_value > best_value:
            best_value = move_value
            best_col = col

    return best_col
