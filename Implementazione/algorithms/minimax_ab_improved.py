"""
Implementazione di Minimax con potatura alpha-beta e decisione imperfette in tempo reale.
(Profondità massima e funzione di valutazione euristica)
L'algoritmo esplora l'intero game tree e restituisce:
  - -1 se lo stato è vincente per il giocatore umano (PLAYER_PIECE),
  - +1 se lo stato è vincente per l'IA (AI_PIECE),
  - 0 se lo stato rappresenta un pareggio.
"""

import numpy as np
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
    """
    Algoritmo minimax con potatura alpha-beta e limite di profondità.

    Parametri:
      - board: stato corrente della board.
      - maximizing_player: True se il turno appartiene all'IA, False al giocatore.
      - alpha: miglior punteggio garantito fino ad ora lungo il cammino dei nodi massimizzanti.
      - beta: miglior punteggio garantito lungo il cammino dei nodi minimizzanti.
      - depth: profondità corrente nella ricorsione.
      - max_depth: profondità massima da esplorare.

    Restituisce:
      Un valore intero che:
        * Valuta lo stato come +1 se vincente per l'IA,
        * -1 se vincente per il giocatore,
        * 0 in caso di pareggio,
        * oppure un punteggio basato sulla funzione euristica se si è raggiunta la profondità massima.
    """

    # Controllo dei casi terminali
    if winning_move(board, PLAYER_PIECE):
        return -1
    if winning_move(board, AI_PIECE):
        return +1
    if is_draw(board):
        return 0

    # Se abbiamo raggiunto il limite massimo di profondità,
    # valutiamo lo stato tramite la funzione euristica.
    if depth == max_depth:
        return score_position(board, AI_PIECE)

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
                break  # beta cut-off
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
                break  # alpha cut-off
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
        # Debug: stampa il punteggio per ogni colonna
        # print(f"Colonna {col}, punteggio: {move_value}")
        if move_value > best_value:
            best_value = move_value
            best_col = col

    return best_col
