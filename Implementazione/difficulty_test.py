import random
import time
from copy import deepcopy

from algorithms.minimax_ab_all_improvements import find_best_move
from board import (
    create_board, drop_piece, is_valid_location, get_next_open_row,
    winning_move, PLAYER_PIECE, AI_PIECE, ROWS, COLS
)
from utils import DIFFICULTY_LEVELS

class DecreaseParameters:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.moves_made = 0
        self.DIFFICULTY_LEVELS = {
            1: {
                'max_depth': 5,
                'beam_width': 4,
                'heuristic_weights': {
                    'win': 10000,
                    'three_in_a_row': 100,
                    'two_in_a_row': 50,
                    'block_opponent_win': 100,
                    'block_opponent_three': 45
                },
                'time_limit': 1.0,
                'center_score_map': [3, 4, 5, 5, 5, 4, 3]
            }
        }
        self.difficulty_params = self.DIFFICULTY_LEVELS[self.difficulty]

    def update_parameters(self):
        self.moves_made += 1
        if self.moves_made <= 4:
            self.difficulty_params['max_depth'] = 5
            self.difficulty_params['beam_width'] = 4
        elif self.moves_made == 5:
            self.difficulty_params['max_depth'] = 4
            self.difficulty_params['beam_width'] = 2
        elif self.moves_made == 6:
            self.difficulty_params['max_depth'] = 3
            self.difficulty_params['beam_width'] = 4
            self.difficulty_params['heuristic_weights'] = {
                'win': 100,
                'three_in_a_row': 25,
                'two_in_a_row': 10,
                'block_opponent_win': 10,
                'block_opponent_three': 0
            }
        elif self.moves_made == 7:
            self.difficulty_params['max_depth'] = 3
            self.difficulty_params['beam_width'] = 2
            self.difficulty_params['heuristic_weights'] = {
                'win': 100,
                'three_in_a_row': 25,
                'two_in_a_row': 10,
                'block_opponent_win': 5,
                'block_opponent_three': 0
            }
        elif self.moves_made >= 8:
            self.difficulty_params['max_depth'] = 2
            self.difficulty_params['beam_width'] = 2
            self.difficulty_params['heuristic_weights'] = {
                'win': 100,
                'three_in_a_row': 25,
                'two_in_a_row': 10,
                'block_opponent_win': 0,
                'block_opponent_three': 0
            }

        return self.difficulty_params

def print_board(board):
    print("\nScacchiera Finale:")
    for row in board:
        print('|' + '|'.join([' ' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]) + '|')
    print('-' * (2 * COLS + 1))
    print(' ' + ' '.join([str(i) for i in range(COLS)]))


def play_game(ai1_level, ai2_level, verbose=False):

    board = create_board()
    game_over = False
    turn = random.choice([1, 2])
    start_player = "AI1" if turn == 1 else "AI2"

    if verbose:
        print(f"Inizio della partita. {start_player} inizia.")

    ai1_total_time = 0
    ai2_total_time = 0
    ai1_move_count = 0
    ai2_move_count = 0

    first_move = True

    decrease_manager_ai1 = DecreaseParameters(1)
    decrease_manager_ai2 = DecreaseParameters(1)

    ai1_params = DIFFICULTY_LEVELS[ai1_level]
    ai2_params = DIFFICULTY_LEVELS[ai2_level]

    while not game_over:
        if turn == 1:
            # AI1 gioca
            start_time = time.time()
            if first_move:
                col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
                if verbose:
                    print(f"AI1 (Livello {ai1_level}) effettua una mossa casuale nella colonna {col}.")
                first_move = False
            else:
                if ai1_level == 1:
                    ai1_params = decrease_manager_ai1.update_parameters()
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
                col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
                if verbose:
                    print(f"AI2 (Livello {ai2_level}) effettua una mossa casuale nella colonna {col}.")
                first_move = False
            else:
                if ai2_level == 1:
                    ai2_params = decrease_manager_ai2.update_parameters()
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

        if not any(is_valid_location(board, c) for c in range(COLS)):
            if verbose:
                print("Pareggio!")
                print_board(board)
            return "Draw", ai1_total_time, ai2_total_time, ai1_move_count, ai2_move_count, board


def main():
    print("Modulo di Test per Sfidare Due AI di Forza 4")

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
        result, t1, t2, m1, m2, final_board = play_game(ai1_level, ai2_level, verbose=True)
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

    avg_ai1_time = ai1_total_time / ai1_total_moves if ai1_total_moves > 0 else 0
    avg_ai2_time = ai2_total_time / ai2_total_moves if ai2_total_moves > 0 else 0

    total_wins = ai1_wins + ai2_wins
    avg_winning_moves = total_winning_moves / total_wins if total_wins > 0 else 0
    avg_losing_moves = total_losing_moves / total_wins if total_wins > 0 else 0

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


