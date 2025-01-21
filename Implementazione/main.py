import sys
import math
import random
import pygame
from threading import Timer
from algorithms.minimax import find_best_move

# Import delle funzioni e costanti di base
from board import (
    create_board,
    ROWS,
    COLS,
    PLAYER_TURN,
    AI_TURN,
    PLAYER_PIECE,
    AI_PIECE,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    winning_move
)

from gui import (
    init_gui,
    draw_board,
    BLUE,
    BLACK,
    RED,
    YELLOW
)

# Dimensioni grafiche
SQUARESIZE = 100
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE / 2 - 5)

# Variabili di stato globale
game_over = False
not_over = True

def end_game():
    global game_over
    game_over = True
    print("Gioco terminato.")

def main():
    global game_over, not_over

    # 1) Richiedi il nome
    player_name = input("Inserisci il tuo nome: ")
    print(f"Ciao {player_name}!")

    # 2) Inizializza la board e la GUI
    board = create_board()
    screen, my_font = init_gui(width, height)
    draw_board(screen, board, SQUARESIZE, circle_radius, ROWS, COLS)
    pygame.display.update()


    turn = PLAYER_TURN
    game_over = False
    not_over = True

    # Loop principale del gioco
    while not game_over:
        for event in pygame.event.get():
            # Uscita manuale (chiusura finestra)
            if event.type == pygame.QUIT:
                sys.exit()

            # Movimento del mouse (visualizzazione gettone in alto)
            if event.type == pygame.MOUSEMOTION and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                xpos = event.pos[0]
                if turn == PLAYER_TURN:
                    pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE / 2)), circle_radius)
                pygame.display.update()

            # Click del mouse per giocare
            if event.type == pygame.MOUSEBUTTONDOWN and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                if turn == PLAYER_TURN:
                    xpos = event.pos[0]
                    col = int(xpos / SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            print(f"{player_name} VINCE!")
                            label = my_font.render(f"{player_name} WINS!", 1, RED)
                            screen.blit(label, (40, 10))
                            not_over = False
                            t = Timer(3.0, end_game)
                            t.start()

                        draw_board(screen, board, SQUARESIZE, circle_radius, ROWS, COLS)
                        turn += 1
                        turn = turn % 2

                pygame.display.update()

        # Turno dell'IA
        if turn == AI_TURN and not game_over and not_over:
            pygame.time.wait(500)  # Breve attesa per rendere visibile l'azione

            col = find_best_move(board)

            if col is not None and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    print("L'AI VINCE!")
                    label = my_font.render("AI WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()

                draw_board(screen, board, SQUARESIZE, circle_radius, ROWS, COLS)
                turn += 1
                turn = turn % 2

    # Quando il gioco termina, attendi qualche istante e chiudi la finestra
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
