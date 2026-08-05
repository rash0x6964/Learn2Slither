import os
import pygame

ASSET_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
)

FLOOR_LIGHT = (27, 26, 85)
FLOOR_DARK = (7, 15, 43)

DIRECTIONS = ("up", "down", "left", "right")


def _load(name, cell_size):
    path = os.path.join(ASSET_DIR, name)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (cell_size, cell_size))


def _direction_between(from_pos, to_pos):
    dx, dy = to_pos.x - from_pos.x, to_pos.y - from_pos.y
    if dx > 0:
        return "right"
    if dx < 0:
        return "left"
    if dy > 0:
        return "down"
    return "up"


class Renderer:
    def __init__(self, cell_number, cell_size=32):
        pygame.init()
        self.cell_number = cell_number
        self.cell_size = cell_size

        self.head_images = {
            d: _load(f"head_{d}.png", cell_size) for d in DIRECTIONS
        }
        self.tail_images = {
            d: _load(f"tail_{d}.png", cell_size) for d in DIRECTIONS
        }
        self.body_horizontal_image = _load("body_horizontal.png", cell_size)
        self.body_vertical_image = _load("body_vertical.png", cell_size)
        self.body_corner_images = {
            corner: _load(f"body_corner_{corner}.png", cell_size)
            for corner in ("tl", "tr", "bl", "br")
        }
        self.green_apple_image = _load("apple_green.png", cell_size)
        self.red_apple_image = _load("apple_red.png", cell_size)

    def draw_onto(self, surface, game_state, top_left=(0, 0)):
        ox, oy = top_left
        self._draw_floor(surface, ox, oy)
        self._draw_apples(surface, game_state, ox, oy)
        self._draw_snake(surface, game_state.snake, ox, oy)

    def _cell_rect(self, x, y, ox, oy):
        return pygame.Rect(
            ox + int(x) * self.cell_size,
            oy + int(y) * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

    def _draw_floor(self, surface, ox, oy):
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                color = FLOOR_LIGHT if (x + y) % 2 == 0 else FLOOR_DARK
                surface.fill(color, self._cell_rect(x, y, ox, oy))

    def _draw_apples(self, surface, game_state, ox, oy):
        for apple in game_state.green_apples:
            rect = self._cell_rect(apple.position.x, apple.position.y, ox, oy)
            surface.blit(self.green_apple_image, rect.topleft)
        red = game_state.red_apple
        rect = self._cell_rect(red.position.x, red.position.y, ox, oy)
        surface.blit(self.red_apple_image, rect.topleft)

    def _body_sprite_for(self, body, i):
        segment = body[i]
        previous_block = body[i + 1] - segment
        next_block = body[i - 1] - segment

        if previous_block.x == next_block.x:
            return self.body_vertical_image
        if previous_block.y == next_block.y:
            return self.body_horizontal_image

        if (previous_block.x == -1 and next_block.y == -1) or (
            previous_block.y == -1 and next_block.x == -1
        ):
            return self.body_corner_images["tl"]
        if (previous_block.x == -1 and next_block.y == 1) or (
            previous_block.y == 1 and next_block.x == -1
        ):
            return self.body_corner_images["bl"]
        if (previous_block.x == 1 and next_block.y == -1) or (
            previous_block.y == -1 and next_block.x == 1
        ):
            return self.body_corner_images["tr"]
        return self.body_corner_images["br"]

    def _draw_snake(self, surface, snake, ox, oy):
        body = snake.body
        n = len(body)
        for i, segment in enumerate(body):
            rect = self._cell_rect(segment.x, segment.y, ox, oy)
            if i == 0:
                facing = (
                    _direction_between(body[1], body[0]) if n > 1 else "right"
                )
                surface.blit(self.head_images[facing], rect.topleft)
            elif i == n - 1:
                facing = _direction_between(body[i - 1], body[i])
                surface.blit(self.tail_images[facing], rect.topleft)
            else:
                surface.blit(self._body_sprite_for(body, i), rect.topleft)
