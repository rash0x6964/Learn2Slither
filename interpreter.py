WALL, HEAD, BODY, GREEN, RED, EMPTY = "W", "H", "S", "G", "R", "0"


def _cell_char(game_state, x, y):
    n = game_state.cell_number
    if x < 0 or x >= n or y < 0 or y >= n:
        return WALL

    head = game_state.snake.head
    if int(head.x) == x and int(head.y) == y:
        return HEAD

    for segment in game_state.snake.body[1:]:
        if int(segment.x) == x and int(segment.y) == y:
            return BODY

    for apple in game_state.green_apples:
        if int(apple.position.x) == x and int(apple.position.y) == y:
            return GREEN

    red = game_state.red_apple.position
    if int(red.x) == x and int(red.y) == y:
        return RED

    return EMPTY


def get_vision(game_state):
    head = game_state.snake.head
    hx, hy = int(head.x), int(head.y)
    n = game_state.cell_number

    up = [_cell_char(game_state, hx, y) for y in range(hy - 1, -2, -1)]
    down = [_cell_char(game_state, hx, y) for y in range(hy + 1, n + 1)]
    left = [_cell_char(game_state, x, hy) for x in range(hx - 1, -2, -1)]
    right = [_cell_char(game_state, x, hy) for x in range(hx + 1, n + 1)]

    return {"up": up, "down": down, "left": left, "right": right}


def build_vision_lines(game_state):
    head = game_state.snake.head
    hx, hy = int(head.x), int(head.y)
    n = game_state.cell_number

    lines = []
    for y in range(-1, n + 1):
        if y == hy:
            row = "".join(
                _cell_char(game_state, x, y) for x in range(-1, n + 1)
            )
            lines.append(row)
        else:
            lines.append(_cell_char(game_state, hx, y))
    return lines


def print_vision(game_state):
    for line in build_vision_lines(game_state):
        print(line)
