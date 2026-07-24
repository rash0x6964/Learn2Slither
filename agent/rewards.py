REWARD_GREEN_APPLE = 15
REWARD_RED_APPLE = -10
REWARD_STEP = -1
REWARD_GAME_OVER = -50


def compute_reward(info):
    if not info["alive"]:
        return REWARD_GAME_OVER
    if info["ate"] == "green":
        return REWARD_GREEN_APPLE
    if info["ate"] == "red":
        return REWARD_RED_APPLE
    return REWARD_STEP
