from pygame.math import Vector2

ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")

_VECTORS = {
    "UP": Vector2(0, -1),
    "DOWN": Vector2(0, 1),
    "LEFT": Vector2(-1, 0),
    "RIGHT": Vector2(1, 0),
}


def action_to_vector(action):
    try:
        return _VECTORS[action]
    except KeyError:
        raise ValueError(
            f"Invalid action: {action!r}. Must be one of {ACTIONS}"
        )
