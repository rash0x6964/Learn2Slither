import pygame
import random
from pygame.math import Vector2


CELL_SIZE = 40
CELL_NUMBER = 10


class Snake():
    def __init__(self):
        self.body = [Vector2(2, 3), Vector2(3, 3), Vector2(4, 3)]
        self.direction = Vector2(-1, 0)
        self.add_new_block = False

        self.head_up = pygame.image.load(
            'assets/images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'assets/images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'assets/images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'assets/images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'assets/images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'assets/images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'assets/images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'assets/images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'assets/images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'assets/images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'assets/images/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'assets/images/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load(
            'assets/images/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'assets/images/body_bottomleft.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('assets/sounds/crunch.wav')

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def draw(self, screen):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def move(self):
        body_copy = None

        if self.add_new_block:
            body_copy = self.body[:]
            self.add_new_block = False
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy[:]

    def grow(self):
        self.add_new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(2, 3), Vector2(3, 3), Vector2(4, 3)]
        self.direction = Vector2(0, 0)


class Apple():
    def __init__(self):
        self.position = Vector2(random.randint(
            0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))
        self.texture = pygame.image.load("assets/images/apple.png")

    def draw(self, screen):
        x_pos = int(self.position.x * CELL_SIZE)
        y_pos = int(self.position.y * CELL_SIZE)

        block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        screen.blit(self.texture, block_rect)

    def randomize(self):
        self.position = Vector2(random.randint(
            0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))


class GameState:
    def __init__(self):
        self.snake = Snake()
        self.apples = [Apple(), Apple(), Apple()]

    def update(self):
        self.snake.move()
        self.collision()
        self.check_fail()

    def draw(self, screen):
        self.snake.draw(screen)
        for apple in self.apples:
            apple.draw(screen)

    def collision(self):
        for apple in self.apples:
            if apple.position == self.snake.body[0]:
                apple.randomize()
                self.snake.grow()
                self.snake.play_crunch_sound()

        for apple in self.apples:
            if apple.position in self.snake.body[1:]:
                apple.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()

        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.snake.reset()


class UserInterface:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(
            (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
        pygame.display.set_caption("AI Controled Snake Game")

        self.game_state = GameState()

        self.running = True
        self.clock = pygame.time.Clock()

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

    def processInput(self):
        self.move_snake_command = Vector2(0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == self.SCREEN_UPDATE:
                self.game_state.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_UP:
                    self.game_state.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.game_state.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.game_state.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.game_state.snake.direction = Vector2(1, 0)

    def update(self):
        # self.game_state.update(self.move_snake_command)
        pass

    def render(self):
        self.window.fill((175, 215, 70))

        # for unit in self.game_state.units:
        #     self.render_unit(unit)
        self.game_state.draw(self.window)

        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    game = UserInterface()
    game.run()

    pygame.quit()
