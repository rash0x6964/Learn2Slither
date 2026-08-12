import random
from pygame.math import Vector2


class Snake:
    def __init__(self, cell_number):
        self.cell_number = cell_number
        self.body = []
        self.direction = Vector2(0, 0)
        self.add_new_block = False
        self.reset()

    def reset(self):
        margin = 2
        axis = random.choice(("horizontal", "vertical"))
        going_positive = random.choice((True, False))

        if axis == "horizontal":
            x = random.randint(margin, self.cell_number - 1 - margin)
            y = random.randint(0, self.cell_number - 1)
            step = Vector2(1, 0) if going_positive else Vector2(-1, 0)
        else:
            x = random.randint(0, self.cell_number - 1)
            y = random.randint(margin, self.cell_number - 1 - margin)
            step = Vector2(0, 1) if going_positive else Vector2(0, -1)

        head = Vector2(x, y)
        self.body = [head - step * i for i in range(3)]
        self.direction = step
        self.add_new_block = False

    def move(self, direction=None):
        if direction is not None:
            self.direction = direction

        if self.add_new_block:
            body_copy = self.body[:]
            self.add_new_block = False
        else:
            body_copy = self.body[:-1]

        new_head = self.body[0] + self.direction
        body_copy.insert(0, new_head)
        self.body = body_copy
        return new_head

    def grow(self):
        self.add_new_block = True
        return True

    def shrink(self):
        if len(self.body) <= 1:
            self.body = []
            return False
        self.body.pop()
        return True

    @property
    def head(self):
        return self.body[0]

    @property
    def length(self):
        return len(self.body)

    def hit_wall(self):
        head = self.head
        return not (
            0 <= head.x < self.cell_number and 0 <= head.y < self.cell_number
        )

    def hit_self(self):
        return self.head in self.body[1:]


class Apple:
    kind = "apple"

    def __init__(self, cell_number, forbidden_cells=()):
        self.cell_number = cell_number
        self.position = Vector2(0, 0)
        self.randomize(forbidden_cells)

    def randomize(self, forbidden_cells=()):
        forbidden = {(int(c.x), int(c.y)) for c in forbidden_cells}
        while True:
            candidate = Vector2(
                random.randint(0, self.cell_number - 1),
                random.randint(0, self.cell_number - 1),
            )
            if (int(candidate.x), int(candidate.y)) not in forbidden:
                self.position = candidate
                return

    def apply(self, snake):
        raise NotImplementedError


class GreenApple(Apple):
    kind = "green"

    def apply(self, snake):
        return snake.grow()


class RedApple(Apple):
    kind = "red"

    def apply(self, snake):
        return snake.shrink()
