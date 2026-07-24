import json
import os
import random

from interpreter import get_vision
from .action import ACTIONS


def encode_state(vision):
    def first_non_empty(cells):
        for c in cells:
            if c != "0":
                return c
        return "W"

    return (
        first_non_empty(vision["up"]),
        first_non_empty(vision["down"]),
        first_non_empty(vision["left"]),
        first_non_empty(vision["right"]),
    )


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}  # {state: {action: value}}
        self.learning_enabled = True

    def _ensure_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in ACTIONS}

    def state_from_game(self, game_state):
        return encode_state(get_vision(game_state))

    def choose_action(self, state):
        self._ensure_state(state)

        if self.learning_enabled and random.random() < self.epsilon:
            return random.choice(ACTIONS)

        q_values = self.q_table[state]
        best_value = max(q_values.values())
        best_actions = [a for a, v in q_values.items() if v == best_value]
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state):
        if not self.learning_enabled:
            return

        self._ensure_state(state)
        old_value = self.q_table[state][action]

        if next_state is None:
            target = reward
        else:
            self._ensure_state(next_state)
            target = reward + self.gamma * max(
                self.q_table[next_state].values()
            )

        self.q_table[state][action] = old_value + self.alpha * (
            target - old_value
        )

    def set_learning(self, enabled):
        self.learning_enabled = enabled

    def save(self, path):
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        serializable = {
            "|".join(state): actions for state, actions in self.q_table.items()
        }
        with open(path, "w") as f:
            json.dump(serializable, f)

    def load(self, path):
        with open(path) as f:
            serializable = json.load(f)
        self.q_table = {
            tuple(key.split("|")): actions
            for key, actions in serializable.items()
        }
