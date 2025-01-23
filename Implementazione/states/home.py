import pygame
from utils import (
    load_image,
    scale_size,
    scale_position
)



# ===============================================================================
# Classe che gestisce lo stato Home
# ===============================================================================
class HomeState:
    def __init__(self, window):
        self.window = window
        self.screen = window.screen
        # Inizializza HomeGui con la callback per Play
        self.home_gui = HomeGui(self.window, self.on_play_clicked)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.home_gui.handle_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.home_gui.handle_click(event.pos)
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.home_gui.handle_event(event)

    def update(self):
        pass

    def render(self, screen):
        self.home_gui.show_home()

    def on_play_clicked(self, player_name, difficulty):
        from states.game_state import GameState
        self.window.change_state(GameState(self.window, player_name, difficulty))


# ===============================================================================
# Classe che gestisce la grafica dello stato Home
# ===============================================================================
class HomeGui:
    def __init__(self, window, on_play_callback):
        self.base_font_size = 30
        pygame.font.init()
        self.scale = window.get_scale()
        self.difficulty = 1
        self.screen = window.screen
        self.on_play_callback = on_play_callback
        screen_width, screen_height = self.screen.get_size()

        self.load_assets()

        self.hover_difficulty = 0
        self.play_button_hover = False

        self.difficulty_positions = {
            1: scale_position(475, 450, screen_width, screen_height),
            2: scale_position(600, 450, screen_width, screen_height),
            3: scale_position(725, 450, screen_width, screen_height),
        }

    def load_assets(self):
        scale_factor = self.scale
        screen_width, screen_height = self.screen.get_size()

        bg_width, bg_height = scale_size(1300, 1000, screen_width, screen_height)
        self.background = load_image("game_assets/home.png", bg_width, bg_height)

        pieces_image = load_image("game_assets/pieces.png", 202 * scale_factor, 100 * scale_factor)
        self.piece = pieces_image.subsurface((0, 0, 100 * scale_factor, 100 * scale_factor ))

        try:
            self.text_font = pygame.font.Font("game_assets/font.ttf", 40)
        except FileNotFoundError:
            print("Font personalizzato non trovato. Utilizzo di un font di sistema.")
            self.text_font = pygame.font.SysFont("Arial", 40)

        self.text_color = (128, 128, 128)


        self.play_button_image = load_image("game_assets/play_button.png", 354 * scale_factor, 87 * scale_factor)
        play_x, play_y = scale_position(473, 813, screen_width, screen_height)
        self.play_button_rect = pygame.Rect(play_x, play_y,  354 * scale_factor, 87 * scale_factor)

        self.input_label_position = scale_position(500, 550, screen_width, screen_height)
        input_x, input_y = scale_position(473, 650, screen_width, screen_height)
        self.input_box_rect = pygame.Rect(input_x, input_y, 354 * scale_factor , 70 * scale_factor)
        self.input_text = ""
        self.input_active = False
        self.input_color_inactive = (200, 200, 200)
        self.input_color_active = self.text_color
        self.input_color = self.input_color_inactive
        self.difficulty_label_position = scale_position(470, 377, screen_width, screen_height)

    def show_home(self):
        self.screen.blit(self.background, (0, 0))

        self.text_font = pygame.font.Font("game_assets/font.ttf", self.get_scaled_font_size())

        difficulty_label_surface = self.text_font.render("Difficulty:", True, self.text_color)
        self.screen.blit(difficulty_label_surface, self.difficulty_label_position)

        name_label_surface = self.text_font.render("Name:", True, self.text_color)
        name_label_rect = name_label_surface.get_rect(
            midbottom=(self.input_box_rect.left + 60 * self.scale, self.input_box_rect.top - 10)
        )

        self.screen.blit(name_label_surface, name_label_rect.topleft)

        pygame.draw.rect(self.screen, self.input_color, self.input_box_rect, 3, 15)

        input_surface = self.text_font.render(self.input_text, True, self.text_color)
        input_rect = input_surface.get_rect(center=self.input_box_rect.center)
        self.screen.blit(input_surface, input_rect.topleft)

        for level, pos in self.difficulty_positions.items():
            if level <= self.difficulty:
                self.screen.blit(self.piece, pos)

        for level, pos in self.difficulty_positions.items():
            if level <= self.hover_difficulty and level > self.difficulty:
                self.screen.blit(self.piece, pos)

        pygame.draw.rect(self.screen, self.input_color, self.input_box_rect, 3, 15)
        input_surface = self.text_font.render("", True, self.text_color)
        self.screen.blit(input_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 10))

        if self.play_button_hover:
            enlarged_image = pygame.transform.smoothscale(
                self.play_button_image,
                (int(self.play_button_rect.width * 1.02),
                 int(self.play_button_rect.height * 1.02))
            )
            enlarged_rect = enlarged_image.get_rect(center=self.play_button_rect.center)
            self.screen.blit(enlarged_image, enlarged_rect.topleft)
        else:
            self.screen.blit(self.play_button_image, self.play_button_rect.topleft)

    def handle_hover(self, mouse_pos):
        self.hover_difficulty = 0

        for level, rect in self._difficulty_rects().items():
            if rect.collidepoint(mouse_pos):
                self.hover_difficulty = level
                break

        if self.play_button_rect.collidepoint(mouse_pos):
            self.play_button_hover = True
        else:
            self.play_button_hover = False

    def handle_click(self, mouse_pos):
        for level, rect in self._difficulty_rects().items():
            if rect.collidepoint(mouse_pos):
                self.difficulty = level
                break


        if self.play_button_rect.collidepoint(mouse_pos):
            self.on_play_callback(self.input_text, self.difficulty)

        if self.input_box_rect.collidepoint(mouse_pos):
            self.input_active = True
            self.input_color = self.input_color_active
        else:
            self.input_active = False
            self.input_color = self.input_color_inactive

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:

                    self.input_active = False
                    self.input_color = self.input_color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 11:
                        if self.input_text == "Nome":
                            self.input_text = ""
                        self.input_text += event.unicode

    def _difficulty_rects(self):
        piece_size = self.piece.get_size()
        return {
            level: pygame.Rect(pos[0], pos[1], piece_size[0], piece_size[1])
            for level, pos in self.difficulty_positions.items()
        }

    def get_scaled_font_size(self):
        screen_width, screen_height = self.screen.get_size()
        return int(self.base_font_size * min(screen_width, screen_height) / 800)
