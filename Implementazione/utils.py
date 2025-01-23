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

