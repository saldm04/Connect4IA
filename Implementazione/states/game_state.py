import pygame
import sys
import time

import difficulty_levels
from algorithms.minimax_ab_all_improvements import find_best_move

from board import (
    create_board, drop_piece, is_valid_location, get_next_open_row,
    winning_move, PLAYER_PIECE, AI_PIECE, PLAYER_TURN, AI_TURN,
    ROWS, COLS
)

from utils import (
    load_image,
    scale_size,
    scale_position
)


class GameState:

    def __init__(self, window, player_name="no name", difficulty=2):
        self.window = window
        self.screen = window.screen
        self.board = create_board()
        self.turn = PLAYER_TURN
        self.game_over = False
        self.not_over = True
        self.player_name = player_name
        self.difficulty = difficulty
        self.user_wins = 0
        self.ai_wins = 0
        self.game_gui = GameGui(self.window, player_name, self)
        self.xpos = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.not_over:
                if event.type == pygame.MOUSEMOTION:
                    self.game_gui.draw_background()
                    self.game_gui.draw_pieces(self.board)
                    self.game_gui.draw_board_layer()
                    self.xpos = event.pos[0]
                    self.game_gui.draw_active_piece(self.xpos)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn == PLAYER_TURN:
                        xpos = event.pos[0]
                        col = self.game_gui.compute_column(xpos)

                        if is_valid_location(self.board, col):
                            row = get_next_open_row(self.board, col)

                            self.game_gui.animate_drop(self.game_gui.player_piece_img, col, row)
                            drop_piece(self.board, row, col, PLAYER_PIECE)

                            if winning_move(self.board, PLAYER_PIECE):
                                self.end_game("User")
                                continue

                            self.turn = AI_TURN
            elif self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.game_gui.play_again_rect.collidepoint(mouse_pos):
                        self.reset_game()
                    elif self.game_gui.quit_rect.collidepoint(mouse_pos):
                        from states.home import HomeState
                        self.window.change_state(HomeState(self.window))

    def update(self):
        if self.turn == AI_TURN and not self.game_over and self.not_over:
            pygame.time.wait(400)

            difficulty_params = difficulty_levels.DIFFICULTY_LEVELS[self.difficulty]
            max_depth = difficulty_params['max_depth']
            beam_width = difficulty_params['beam_width']
            heuristic_weights = difficulty_params['heuristic_weights']
            time_limit = difficulty_params['time_limit']
            center_score_map = difficulty_params['center_score_map']
            start_time = time.time()
            col = find_best_move(self.board, max_depth, beam_width, heuristic_weights, time_limit, center_score_map)
            end_time = time.time()
            print(f"Tempo di calcolo IA: {end_time - start_time} secondi")

            if col is not None and is_valid_location(self.board, col):
                row = get_next_open_row(self.board, col)
                self.game_gui.animate_drop(self.game_gui.ai_piece_img, col, row)
                drop_piece(self.board, row, col, AI_PIECE)

                if winning_move(self.board, AI_PIECE):
                    self.end_game("AI")
                    return

                self.turn = PLAYER_TURN

    def render(self, screen):
        self.game_gui.render(screen)

    def end_game(self, winner):
        self.game_over = True
        if winner == "User":
            self.user_wins += 1
        elif winner == "AI":
            self.ai_wins += 1
        self.not_over = False
        pygame.display.update()

    def reset_game(self):
        self.board = create_board()
        self.turn = PLAYER_TURN
        self.game_over = False
        self.not_over = True
        self.xpos = 0
        pygame.display.update()

class GameGui:

    def __init__(self, window, player_name, game_state):
        self.base_font_size = 17
        pygame.font.init()
        self.scale = window.get_scale()
        self.screen = window.screen
        self.player_name = player_name
        self.game_state = game_state
        self.load_assets()
        self.play_again_rect = None
        self.quit_rect = None

    def load_assets(self):
        scale_factor = self.scale
        screen_width, screen_height = self.screen.get_size()

        bg_width, bg_height = scale_size(1300, 1000, screen_width, screen_height)
        self.background = load_image("game_assets/game_background.png", bg_width, bg_height)

        self.board_img = load_image("game_assets/board.png", int(1800 / 2) * scale_factor, int(1600 / 2) * scale_factor)

        pieces_image = load_image("game_assets/pieces.png", 202 * (scale_factor + 0.03), 100 * (scale_factor + 0.03))

        self.player_piece_img = pieces_image.subsurface((0, 0, 100 * (scale_factor + 0.04), 100 * (scale_factor + 0.03)))
        self.ai_piece_img = pieces_image.subsurface((102 * (scale_factor + 0.03), 0, 100 * (scale_factor + 0.03), 100 * (scale_factor + 0.03)))

    def draw_background(self):
        screen_width, screen_height = self.screen.get_size()
        text_color = (0, 0, 0)  # Colore migliorato

        self.text_font = pygame.font.Font("game_assets/font.ttf", self.get_scaled_font_size())


        user_name_position = scale_position(32.9, 333.9, screen_width, screen_height)
        user_win_position = scale_position(32.9, 377.9, screen_width, screen_height)
        ai_name_position = scale_position(1132.9, 333.9, screen_width, screen_height)
        ai_win_position = scale_position(1132.9, 377.9, screen_width, screen_height)

        #user_text = f"{self.player_name} \nWin: {self.game_state.user_wins}"
        user_text = f"{self.player_name.upper() if self.player_name != '' else 'no name'}"
        ai_text = "AI"

        user_render = self.text_font.render(user_text, True, text_color)
        ai_render = self.text_font.render(ai_text, True, text_color)
        ai_win_render = self.text_font.render(f"Win: {self.game_state.ai_wins}", True, text_color)
        user_win_render = self.text_font.render(f"Win: {self.game_state.user_wins}", True, text_color)

        self.screen.blit(self.background, (0, 0))

        self.screen.blit(user_render, user_name_position)
        self.screen.blit(ai_render, ai_name_position)
        self.screen.blit(user_win_render, user_win_position)
        self.screen.blit(ai_win_render, ai_win_position)

    def draw_board_layer(self):
        self.screen.blit(self.board_img, (200 * self.scale, 170 * self.scale))

    def draw_pieces(self, board):
        ped_size = 100 * self.scale
        margin = int((25.6 / 2) * self.scale)
        grid_origin = (int((524.5 / 2) * self.scale), int(int(473.7 / 2) * self.scale))

        rows = len(board)
        cols = len(board[0])
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 0:
                    continue
                pos_x = grid_origin[0] + c * (ped_size + margin)
                pos_y = grid_origin[1] + r * (ped_size + margin)
                if board[r][c] == 1:
                    self.screen.blit(self.player_piece_img, (pos_x, pos_y))
                elif board[r][c] == 2:
                    self.screen.blit(self.ai_piece_img, (pos_x, pos_y))

    def draw_active_piece(self, x):
        active_area_left = (624.5 / 2) * self.scale
        active_area_right = (1974.5 / 2) * self.scale
        ped_size = 100 * self.scale

        if x < active_area_left:
            x = active_area_left
        elif x > active_area_right:
            x = active_area_right

        offset = ped_size // 2
        self.screen.blit(self.player_piece_img, (x - offset, int(100 / 2) * self.scale))

    def compute_column(self, xpos):
        grid_origin_x = int((524.5 / 2) * self.scale)
        pedina_size = (100 * self.scale)
        margin = int((25/2) * self.scale)

        col = int((xpos - grid_origin_x) // (pedina_size + margin))
        if col < 0:
            col = 0
        elif col >= COLS:
            col = COLS - 1
        return col

    def get_scaled_font_size(self):
        screen_width, screen_height = self.screen.get_size()
        return int(self.base_font_size * min(screen_width, screen_height) / 800)

    def draw_overlay(self, winner):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        overlay_font = pygame.font.Font("game_assets/font.ttf", self.get_scaled_font_size() * 2)
        winner_text = f"Winner: {winner}"
        winner_render = overlay_font.render(winner_text, True, (255, 255, 255))
        winner_rect = winner_render.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 100))
        self.screen.blit(winner_render, winner_rect)

        button_font = pygame.font.Font("game_assets/font.ttf", self.get_scaled_font_size())
        play_again_text = "Play Again"
        play_again_render = button_font.render(play_again_text, True, (255, 255, 255))
        play_again_rect = play_again_render.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(play_again_render, play_again_rect)

        quit_text = "Quit"
        quit_render = button_font.render(quit_text, True, (255, 255, 255))
        quit_rect = quit_render.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        self.screen.blit(quit_render, quit_rect)

        self.play_again_rect = play_again_rect
        self.quit_rect = quit_rect

    def animate_drop(self, piece_img, col, target_row):
        ped_size = 100 * self.scale
        margin = int((25.6 / 2) * self.scale)
        grid_origin = (int((524.5 / 2) * self.scale), int(int(473.5 / 2) * self.scale))
        pos_x = grid_origin[0] + col * (ped_size + margin)
        pos_y_start = grid_origin[1] - ped_size
        pos_y_end = grid_origin[1] + target_row * (ped_size + margin)

        frames = 60
        clock = pygame.time.Clock()

        for frame in range(frames):
            progress = frame / frames
            current_y = pos_y_start + (pos_y_end - pos_y_start) * progress
            self.draw_background()
            self.draw_pieces(self.game_state.board)
            self.screen.blit(piece_img, (pos_x, current_y + (12 * self.scale )))
            self.draw_board_layer()
            pygame.display.update()
            clock.tick(60)

    def render(self, screen):
        if self.game_state.not_over:
            self.draw_background()
            self.draw_pieces(self.game_state.board)
            self.draw_board_layer()
            if self.game_state.turn != AI_TURN:
                self.draw_active_piece(self.game_state.xpos)
        else:
            self.draw_background()
            self.draw_pieces(self.game_state.board)
            self.draw_board_layer()
            if self.game_state.turn != AI_TURN:
                self.draw_active_piece(self.game_state.xpos)
            winner = "Utente" if self.game_state.turn == PLAYER_TURN else "AI"
            self.draw_overlay(winner)
        pygame.display.update()
