import pygame
from pygame.math import Vector2

from environment.game_state import GameState
from environment.renderer import Renderer


DIRECTIONS = {
    pygame.K_UP: Vector2(0, -1),
    pygame.K_DOWN: Vector2(0, 1),
    pygame.K_LEFT: Vector2(-1, 0),
    pygame.K_RIGHT: Vector2(1, 0),
}


class ManualPlay:
    def __init__(self, cell_number=10, tick_ms=150):
        self.game_state = GameState(cell_number)
        self.renderer = Renderer(self.game_state)
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.tick_event, tick_ms)
        self.next_direction = None

    def run(self):
        while self.running:
            self._handle_events()
            self.renderer.draw(self.game_state)
            self.clock.tick(60)
        self.renderer.close()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.tick_event:
                self._step()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in DIRECTIONS:
                    self.next_direction = DIRECTIONS[event.key]

    def _step(self):
        info = self.game_state.step(self.next_direction)
        self.next_direction = None
        if not info["alive"]:
            print(
                f"Game over, max length = {info['max_length']}, "
                f"max duration = {info['steps']}"
            )
            self.game_state.reset()


if __name__ == "__main__":
    ManualPlay().run()
