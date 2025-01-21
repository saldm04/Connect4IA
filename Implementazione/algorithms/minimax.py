"""
Implementazione di Minimax "puro" (senza profondità massima, senza alpha-beta)
che esplora l'intero game tree. Viene restituito:
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
    drop_piece
)

def is_draw(board):
    """Restituisce True se la board non ha mosse valide."""
    return len(get_valid_locations(board)) == 0

def clone_board(board):
    """
    Crea e restituisce una copia della board.
    """
    return board.copy()

def pure_minimax(board, maximizing_player):

    # Se la partita è finita, valutiamo l'esito
    if winning_move(board, PLAYER_PIECE):
        return -1  # Vantaggio per il giocatore umano
    if winning_move(board, AI_PIECE):
        return +1  # Vantaggio per l'IA
    if is_draw(board):
        return 0

    #turno dell'IA
    if maximizing_player:
        best_value = float('-inf')
        for col in get_valid_locations(board):
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, AI_PIECE)
            value = pure_minimax(new_board, False)
            best_value = max(best_value, value)
        return best_value
    else:
        
        #turno dell'utente
        best_value = float('inf')
        for col in get_valid_locations(board):
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, PLAYER_PIECE)
            value = pure_minimax(new_board, True)
            best_value = min(best_value, value)
        return best_value

def find_best_move(board):
    """
    Restituisce la colonna migliore per l'IA (AI_PIECE) valutando l'intero game tree.
    In caso di più mosse equivalenti, ne sceglie quella con il valore massimo.
    """
    best_value = float('-inf')
    best_col = None

    for col in get_valid_locations(board):
        new_board = clone_board(board)
        row = get_next_open_row(new_board, col)
        drop_piece(new_board, row, col, AI_PIECE)
        move_value = pure_minimax(new_board, False)
        if move_value > best_value:
            best_value = move_value
            best_col = col

    return best_col
