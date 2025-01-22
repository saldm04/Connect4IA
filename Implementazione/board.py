import numpy as np

# Costanti di base per la gestione della board
ROWS = 6
COLS = 7

PLAYER_TURN = 0
AI_TURN = 1

PLAYER_PIECE = 1
AI_PIECE = 2


def create_board():
    """
    Crea una matrice 6x7 (row x col) inizializzata a 0.
    """
    board = np.zeros((ROWS, COLS))
    return board


def drop_piece(board, row, col, piece):
    """
    Inserisce la pedina nella posizione [row, col].
    """
    board[row][col] = piece


def is_valid_location(board, col):
    """
    Controlla se la colonna non è piena (riga più alta a 0).
    """
    return board[0][col] == 0


def get_next_open_row(board, col):
    """
    Restituisce l'indice della prima riga libera (dall'alto verso il basso)
    nella colonna.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    """
    Verifica se il giocatore ha fatto '4 in fila'.
    Ritorna True se esiste una combinazione vincente.
    """
    # Controllo orizzontale
    for c in range(COLS - 3):
        for r in range(ROWS):
            if (board[r][c] == piece and board[r][c + 1] == piece and
                    board[r][c + 2] == piece and board[r][c + 3] == piece):
                return True

    # Controllo verticale
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and
                    board[r + 2][c] == piece and board[r + 3][c] == piece):
                return True

    # Controllo diagonale positiva
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                return True

    # Controllo diagonale negativa
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if (board[r][c] == piece and board[r - 1][c - 1] == piece and
                    board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece):
                return True

    return False


def get_valid_locations(board):
    """
    Restituisce le colonne valide in cui è possibile inserire un pezzo.
    """
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    """
    Ritorna True se la board è in uno stato terminale (vittoria giocatore/AI o pareggio).
    """
    return (winning_move(board, PLAYER_PIECE) or
            winning_move(board, AI_PIECE) or
            len(get_valid_locations(board)) == 0)


# =======================================================================
# Funzioni di valutazione (euristiche)
# =======================================================================

def evaluate_window(window, piece):
    """
    Valuta una finestra (lista di 4 celle) in base a quanti pezzi del giocatore (piece)
    e dell'avversario contiene.

      - Se la finestra contiene 4 pezzi del giocatore: +100
      - Se la finestra contiene 3 pezzi del giocatore e 1 cella vuota: +10
      - Se la finestra contiene 2 pezzi del giocatore e 2 celle vuote: +2
      - Se la finestra contiene 3 pezzi dell'avversario e 1 cella vuota: -5
      - Se la finestra contiene 2 pezzi dell'avversario e 2 celle vuote: -1

    Parametri:
      window : list di 4 elementi della board
      piece  : il giocatore per cui valutare la finestra (PLAYER_PIECE o AI_PIECE)
    """
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 5
    elif window.count(opponent_piece) == 2 and window.count(0) == 2:
        score -= 1

    return score


def score_position(board, piece):
    """
    Calcola un punteggio complessivo per la board in favore del giocatore 'piece',
    tenendo in considerazione:
      - Il controllo della colonna centrale.
      - La valutazione di tutte le possibili finestre (orizzontali, verticali e diagonali)
        di 4 celle.
    """
    score = 0

    # 1. Punteggio per il controllo della colonna centrale (bonus aumentato)
    center_col = COLS // 2
    center_array = [int(i) for i in list(board[:, center_col])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # 2. Punteggio per finestre orizzontali
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # 3. Punteggio per finestre verticali
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # 4. Punteggio per finestre diagonali (positiva)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # 5. Punteggio per finestre diagonali (negativa)
    for r in range(3, ROWS):
        for c in range(3, COLS):
            window = [board[r - i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score
