from pygame.math import Vector2

ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
_VECTORS = {
    "UP": Vector2(0, -1),
    "DOWN": Vector2(0, 1),
    "LEFT": Vector2(-1, 0),
    "RIGHT": Vector2(1, 0),
}

FEATURES_PER_DIRECTION = 3
STATE_DIM = len(ACTIONS) * FEATURES_PER_DIRECTION

REWARD_GREEN_APPLE = 15
REWARD_RED_APPLE = -10
REWARD_STEP = -1
REWARD_GAME_OVER = -50


def action_to_vector(action):
    try:
        return _VECTORS[action]
    except KeyError:
        raise ValueError(
            f"Invalid action: {action!r}. Must be one of {ACTIONS}"
        )


def _direction_features(cells):
    danger = 1.0 if cells and cells[0] in ("W", "S") else 0.0

    green_signal = 0.0
    red_signal = 0.0
    for i, c in enumerate(cells):
        if c in ("W", "S"):
            break
        if c == "G" and green_signal == 0.0:
            green_signal = 1.0 / (i + 1)
        if c == "R" and red_signal == 0.0:
            red_signal = 1.0 / (i + 1)

    return [danger, green_signal, red_signal]


def encode_state_vector(vision):
    features = []
    for direction in ACTIONS:
        features.extend(_direction_features(vision[direction]))
    return features


def compute_reward(info):
    if not info["alive"]:
        return REWARD_GAME_OVER
    if info["ate"] == "green":
        return REWARD_GREEN_APPLE
    if info["ate"] == "red":
        return REWARD_RED_APPLE
    return REWARD_STEP
