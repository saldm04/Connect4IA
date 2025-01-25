import pygame

def load_image(path, width, height):
    try:
        original_image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Errore nel caricamento dell'immagine {path}: {e}")
        raise SystemExit(e)

    return pygame.transform.smoothscale(original_image, (width, height))

def scale_size(original_width, original_height, screen_width, screen_height):
    scale_w = screen_width / original_width
    scale_h = screen_height / original_height
    scale = min(scale_w, scale_h)
    return int(original_width * scale), int(original_height * scale)


def scale_position(original_x, original_y, screen_width, screen_height):
    base_width, base_height = 1300, 1000
    scaled_x = int(original_x * screen_width / base_width)
    scaled_y = int(original_y * screen_height / base_height)
    return scaled_x, scaled_y


DIFFICULTY_LEVELS = {
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
    },
    2: {
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
    },
    3: {
        'max_depth': 7,
        'beam_width': 6,
        'heuristic_weights': {
            'win': 10000,
            'three_in_a_row': 200,
            'two_in_a_row': 100,
            'block_opponent_win': 210,
            'block_opponent_three': 100
        },
        'time_limit': 1.2,
        'center_score_map': [6, 8, 10, 14, 10, 8, 6]
    }
}