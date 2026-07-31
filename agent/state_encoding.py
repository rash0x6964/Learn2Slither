DIRECTIONS = ("up", "down", "left", "right")
FEATURES_PER_DIRECTION = 3
STATE_DIM = len(DIRECTIONS) * FEATURES_PER_DIRECTION


def _direction_features(cells):
    danger = 1.0 if cells and cells[0] in ("W", "S") else 0.0

    green_signal = 0.0
    red_signal = 0.0
    for i, c in enumerate(cells):
        if c in ("W", "S"):
            break  # view is blocked from here on, nothing past this counts
        if c == "G" and green_signal == 0.0:
            green_signal = 1.0 / (i + 1)
        if c == "R" and red_signal == 0.0:
            red_signal = 1.0 / (i + 1)

    return [danger, green_signal, red_signal]


def encode_state_vector(vision):
    features = []
    for direction in DIRECTIONS:
        features.extend(_direction_features(vision[direction]))
    return features
