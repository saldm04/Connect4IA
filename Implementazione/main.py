import pygame

SCALE = 0.65
WINDOW_WIDTH = int(1300 * SCALE)
WINDOW_HEIGHT = int(1000 * SCALE)

class Window:
    FPS = 60

    def __init__(self):
        self.scale = SCALE
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect4IA")
        self.clock = pygame.time.Clock()
        from states.home import HomeState
        self.current_state = HomeState(self)

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            self.current_state.handle_events()
            self.current_state.update()
            self.current_state.render(self.screen)
            pygame.display.flip()

    def change_state(self, new_state):
        self.current_state = new_state

    def get_scale(self):
        return self.scale

def main():
    pygame.init()
    window = Window()
    window.run()
    pygame.quit()

if __name__ == "__main__":
    main()
