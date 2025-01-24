"""
Implementazione di Minimax con potatura alpha-beta, approfondimento iterativo,
ordinamento dinamico delle mosse e potatura in avanti (beam search).
"""
from board import (
    PLAYER_PIECE,
    AI_PIECE,
    winning_move,
    get_valid_locations,
    get_next_open_row,
    drop_piece,
    score_position,
)


# --- Funzioni di utilità ---

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


def order_moves(board, moves, piece, heuristic_weights, center_score_map):
    """
    Ordina le mosse in base all'euristica (score_position) per la board ottenuta
    applicando ciascuna mossa. Le mosse sono ordinate in ordine decrescente se
    'piece' è quello dell'IA, altrimenti in ordine crescente.
    """
    scored_moves = []
    for col in moves:
        new_board = clone_board(board)
        row = get_next_open_row(new_board, col)
        drop_piece(new_board, row, col, piece)
        score = score_position(new_board, piece, heuristic_weights, center_score_map)
        scored_moves.append((score, col))
    scored_moves.sort(key=lambda x: x[0], reverse=True)
    # Restituisce solo la lista delle colonne ordinate
    ordered_moves = [col for (_, col) in scored_moves]
    return ordered_moves


# --- Minimax con potatura alpha-beta, beam search e approfondimento iterativo ---

def minimax_alpha_beta(board, maximizing_player, alpha, beta, depth, max_depth, beam_width, heuristic_weights, center_score_map):

    # Casi terminali
    if winning_move(board, PLAYER_PIECE):
        return -10000
    if winning_move(board, AI_PIECE):
        return +10000
    if is_draw(board):
        return 0

    if depth == max_depth:
        return score_position(board, AI_PIECE, heuristic_weights, center_score_map)

    valid_moves = get_valid_locations(board)

    # Ordinamento dinamico delle mosse
    # Se è il turno dell'IA, ordina in ordine decrescente, altrimenti in ordine crescente.
    current_piece = AI_PIECE if maximizing_player else PLAYER_PIECE
    ordered_moves = order_moves(board, valid_moves, current_piece, heuristic_weights, center_score_map)
    # Applica la beam search: considera solo le prime "beam_width" mosse
    ordered_moves = ordered_moves[:beam_width] if beam_width < len(ordered_moves) else ordered_moves
    if maximizing_player:
        best_value = float('-inf')
        for col in ordered_moves:
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, AI_PIECE)
            value = minimax_alpha_beta(new_board, False, alpha, beta, depth + 1, max_depth, beam_width, heuristic_weights, center_score_map)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break  # beta cut-off
        return best_value
    else:
        best_value = float('inf')
        for col in ordered_moves:
            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, PLAYER_PIECE)
            value = minimax_alpha_beta(new_board, True, alpha, beta, depth + 1, max_depth, beam_width, heuristic_weights, center_score_map)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if alpha >= beta:
                break  # alpha cut-off
        return best_value


import time


def iterative_deepening_minimax(board, max_depth, beam_width, heuristic_weights, time_limit, center_score_map):
    """
    Approfondimento iterativo con controllo di tempo: esegue la ricerca iterativamente
    da profondità 1 fino a max_depth, fermandosi se supera il limite di tempo di un secondo.

    Restituisce la migliore mossa trovata in base all'ultima iterazione completata.
    """
    best_move = None
    start_time = time.time()  # Tempo iniziale

    for current_depth in range(1, max_depth + 1):
        best_value = float('-inf')
        valid_moves = get_valid_locations(board)
        ordered_moves = order_moves(board, valid_moves, AI_PIECE, heuristic_weights, center_score_map)
        ordered_moves = ordered_moves[:beam_width] if beam_width < len(ordered_moves) else ordered_moves

        for col in ordered_moves:
            # Controllo del tempo
            if time.time() - start_time > time_limit:
                # Superato il limite di tempo, restituisce la migliore mossa trovata
                return best_move

            new_board = clone_board(board)
            row = get_next_open_row(new_board, col)
            drop_piece(new_board, row, col, AI_PIECE)
            move_value = minimax_alpha_beta(new_board, False, float('-inf'), float('inf'), 1, current_depth, beam_width, heuristic_weights, center_score_map)
            if move_value > best_value:
                best_value = move_value
                best_move = col

    return best_move

def find_best_move(board, max_depth, beam_width, heuristic_weights, time_limit, center_score_map):
    """
    Determina la migliore mossa per l'IA (AI_PIECE) in base allo stato corrente della board,
    utilizzando approfondimento iterativo, ordinamento dinamico e potatura in avanti (beam search).

    Parametri:
      - board: lo stato corrente della board.
      - max_depth: profondità massima di esplorazione per l'approfondimento iterativo.
      - beam_width: larghezza della beam search.
      - heuristic_weights: pesi per la funzione di valutazione.
      - time_limit: limite di tempo per l'approfondimento iterativo
      - center_score_map: moltiplicatori per le pedine nelle colonne centrali

    Restituisce:
      - best_col: indice della colonna che rappresenta la mossa ottimale per l'IA.

    """
    return iterative_deepening_minimax(board, max_depth, beam_width, heuristic_weights, time_limit, center_score_map)