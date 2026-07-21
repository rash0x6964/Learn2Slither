import pygame


BLOCK_SIZE = 24


class GameState:
    def __init__(self):
        self.x = 5 * BLOCK_SIZE - 20
        self.y = 5 * BLOCK_SIZE - 20

    def update(self, move_command_x, move_command_y):
        self.x += move_command_x
        self.y += move_command_y


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Controled Snake Game")

        self.running = True
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(
            (10 * BLOCK_SIZE, 10 * BLOCK_SIZE))

        self.game_state = GameState()
        self.move_command_x = 0
        self.move_command_y = 0

    def processInput(self):

        self.move_command_x = 0
        self.move_command_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_UP:
                    self.move_command_y -= 5
                elif event.key == pygame.K_DOWN:
                    self.move_command_y += 5
                elif event.key == pygame.K_LEFT:
                    self.move_command_x -= 5
                elif event.key == pygame.K_RIGHT:
                    self.move_command_x += 5

    def update(self):
        self.game_state.update(self.move_command_x, self.move_command_y)

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(
            self.window,
            (0, 0, 255),
            (self.game_state.x, self.game_state.y, 20, 20),
        )
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()
