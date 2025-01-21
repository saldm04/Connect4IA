import pygame

# Colori
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def init_gui(width, height):
    """
    Inizializza la finestra pygame e restituisce lo schermo e il font da usare.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont("monospace", 75)
    return screen, font

def draw_board(screen, board, SQUARESIZE, circle_radius, ROWS, COLS):
    """
    Disegna il tabellone sullo schermo Pygame.
    """
    for c in range(COLS):
        for r in range(ROWS):
            # rettangolo blu
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            # cerchio nero o colorato
            if board[r][c] == 0:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                    ),
                    circle_radius,
                )
            elif board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                    ),
                    circle_radius,
                )
            else:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                    ),
                    circle_radius,
                )

    pygame.display.update()
