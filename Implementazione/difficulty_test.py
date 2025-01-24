import random
import time
from copy import deepcopy

# Importa le funzioni necessarie dai tuoi moduli esistenti
from algorithms.minimax_ab_all_improvements import find_best_move
from board import (
    create_board, drop_piece, is_valid_location, get_next_open_row,
    winning_move, PLAYER_PIECE, AI_PIECE, ROWS, COLS
)
from difficulty_levels import DIFFICULTY_LEVELS


def print_board(board):
    """Stampa la scacchiera nel terminale."""
    print("\nScacchiera Finale:")
    for row in board:
        print('|' + '|'.join([' ' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]) + '|')
    print('-' * (2 * COLS + 1))
    print(' ' + ' '.join([str(i) for i in range(COLS)]))


def play_game(ai1_level, ai2_level, verbose=False):
    """
    Gioca una singola partita tra due AI di diversi livelli.

    Parametri:
      - ai1_level: Livello di difficoltà per AI1 (1, 2, 3).
      - ai2_level: Livello di difficoltà per AI2 (1, 2, 3).
      - verbose: Se True, stampa dettagli della partita.

    Restituisce:
      - Vincitore della partita ("AI1", "AI2" o "Draw").
      - Tempo totale di risposta di AI1.
      - Tempo totale di risposta di AI2.
      - Numero di mosse effettuate da AI1.
      - Numero di mosse effettuate da AI2.
      - Stato finale della scacchiera.
    """
    board = create_board()
    game_over = False
    turn = random.choice([1, 2])  # 1 per AI1, 2 per AI2
    start_player = "AI1" if turn == 1 else "AI2"

    if verbose:
        print(f"Inizio della partita. {start_player} inizia.")

    # Variabili per i tempi di risposta e conteggio mosse
    ai1_total_time = 0
    ai2_total_time = 0
    ai1_move_count = 0
    ai2_move_count = 0

    # Flag per determinare se è la prima mossa
    first_move = True

    # Ottieni parametri da DIFFICULTY_LEVELS
    ai1_params = DIFFICULTY_LEVELS[ai1_level]
    ai2_params = DIFFICULTY_LEVELS[ai2_level]

    while not game_over:
        if turn == 1:
            # AI1 gioca
            start_time = time.time()
            if first_move:
                # Mossa di apertura casuale
                col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
                if verbose:
                    print(f"AI1 (Livello {ai1_level}) effettua una mossa casuale nella colonna {col}.")
                first_move = False
            else:
                # Mossa basata sull'AI
                col = find_best_move(deepcopy(board), ai1_params['max_depth'], ai1_params['beam_width'],
                                     ai1_params['heuristic_weights'], ai1_params['time_limit'],
                                     ai1_params['center_score_map'])
                if verbose:
                    print(f"AI1 (Livello {ai1_level}) ha scelto la colonna {col}.")
            move_time = time.time() - start_time
            ai1_total_time += move_time
            ai1_move_count += 1
            if verbose:
                print(f"Tempo di risposta AI1: {move_time:.4f} secondi.")

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if verbose:
                    print(f"AI1 ha posizionato una pedina in riga {row}, colonna {col}.")

                if winning_move(board, PLAYER_PIECE):
                    if verbose:
                        print("AI1 vince!")
                        print_board(board)
                    return "AI1", ai1_total_time, ai2_total_time, ai1_move_count, ai2_move_count, board

                turn = 2
        else:
            # AI2 gioca
            start_time = time.time()
            if first_move:
                # Mossa di apertura casuale
                col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
                if verbose:
                    print(f"AI2 (Livello {ai2_level}) effettua una mossa casuale nella colonna {col}.")
                first_move = False
            else:
                # Mossa basata sull'AI
                col = find_best_move(deepcopy(board), ai2_params['max_depth'], ai2_params['beam_width'],
                                     ai2_params['heuristic_weights'], ai2_params['time_limit'],
                                     ai2_params['center_score_map'])
                if verbose:
                    print(f"AI2 (Livello {ai2_level}) ha scelto la colonna {col}.")
            move_time = time.time() - start_time
            ai2_total_time += move_time
            ai2_move_count += 1
            if verbose:
                print(f"Tempo di risposta AI2: {move_time:.4f} secondi.")

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if verbose:
                    print(f"AI2 ha posizionato una pedina in riga {row}, colonna {col}.")

                if winning_move(board, AI_PIECE):
                    if verbose:
                        print("AI2 vince!")
                        print_board(board)
                    return "AI2", ai1_total_time, ai2_total_time, ai1_move_count, ai2_move_count, board

                turn = 1

        # Controlla se la scacchiera è piena
        if not any(is_valid_location(board, c) for c in range(COLS)):
            if verbose:
                print("Pareggio!")
                print_board(board)
            return "Draw", ai1_total_time, ai2_total_time, ai1_move_count, ai2_move_count, board


def main():
    print("Modulo di Test per Sfidare Due AI di Forza 4")

    # Input dell'utente
    while True:
        try:
            ai1_level = int(input("Inserisci il livello della AI1 (1, 2, 3): "))
            if ai1_level not in [1, 2, 3]:
                raise ValueError
            ai2_level = int(input("Inserisci il livello della AI2 (1, 2, 3): "))
            if ai2_level not in [1, 2, 3]:
                raise ValueError
            num_matches = int(input("Quante partite vuoi eseguire? "))
            if num_matches <= 0:
                raise ValueError
            break
        except ValueError:
            print("Per favore, inserisci valori numerici validi (livelli: 1, 2, 3; partite: >0).")

    # Variabili per le statistiche
    ai1_wins = 0
    ai2_wins = 0
    draws = 0
    ai1_total_time = 0
    ai2_total_time = 0
    ai1_total_moves = 0
    ai2_total_moves = 0
    total_winning_moves = 0
    total_losing_moves = 0

    print("\nInizio del Test...\n")

    for match in range(1, num_matches + 1):
        print(f"--- Partita {match} ---")
        result, t1, t2, m1, m2, final_board = play_game(ai1_level, ai2_level, verbose=False)
        if result == "AI1":
            ai1_wins += 1
            total_winning_moves += m1
            total_losing_moves += m2
            print("Risultato: AI1 ha vinto questa partita.")
            print(f"Mosse AI1: {m1}, Mosse AI2: {m2}\n")
        elif result == "AI2":
            ai2_wins += 1
            total_winning_moves += m2
            total_losing_moves += m1
            print("Risultato: AI2 ha vinto questa partita.")
            print(f"Mosse AI1: {m1}, Mosse AI2: {m2}\n")
        else:
            draws += 1
            print("Risultato: Pareggio.")
            print(f"Mosse AI1: {m1}, Mosse AI2: {m2}\n")
        ai1_total_time += t1
        ai2_total_time += t2
        ai1_total_moves += m1
        ai2_total_moves += m2

    # Calcolo dei tempi medi per mossa
    avg_ai1_time = ai1_total_time / ai1_total_moves if ai1_total_moves > 0 else 0
    avg_ai2_time = ai2_total_time / ai2_total_moves if ai2_total_moves > 0 else 0

    # Calcolo delle mosse medie per vincere
    total_wins = ai1_wins + ai2_wins
    avg_winning_moves = total_winning_moves / total_wins if total_wins > 0 else 0
    avg_losing_moves = total_losing_moves / total_wins if total_wins > 0 else 0

    # Output dei risultati
    print("Test Completato!\n")
    print(f"Numero di Partite: {num_matches}")
    print(f"Vittorie AI1 (Livello {ai1_level}): {ai1_wins}")
    print(f"Vittorie AI2 (Livello {ai2_level}): {ai2_wins}")
    print(f"Pareggi: {draws}\n")

    print(f"Tempo Medio di Risposta AI1: {avg_ai1_time:.4f} secondi per mossa")
    print(f"Tempo Medio di Risposta AI2: {avg_ai2_time:.4f} secondi per mossa\n")

    if total_wins > 0:
        print(f"Mosse Medie per Vincere: {avg_winning_moves:.2f}")
    else:
        print("Nessuna vittoria registrata per calcolare le mosse medie.")


if __name__ == "__main__":
    main()