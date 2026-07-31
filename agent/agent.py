import random
from collections import deque

import torch
import torch.nn as nn
import torch.optim as optim

from interpreter import get_vision
from .action import ACTIONS
from .network import QNetwork
from .state_encoding import encode_state_vector, STATE_DIM


class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state):
        self.buffer.append((state, action, reward, next_state))

    def sample(self, batch_size):
        batch_size = min(batch_size, len(self.buffer))
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


class QLearningAgent:
    def __init__(
        self,
        alpha=0.001,
        gamma=0.9,
        epsilon=0.2,
        hidden_dim=64,
        batch_size=64,
        buffer_capacity=10000,
        target_update_every=200,
    ):
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_enabled = True
        self.batch_size = batch_size
        self.target_update_every = target_update_every
        self._updates_done = 0

        self.device = torch.device("cpu")
        self.network = QNetwork(STATE_DIM, len(ACTIONS), hidden_dim).to(
            self.device
        )
        self.target_network = QNetwork(STATE_DIM, len(ACTIONS), hidden_dim).to(
            self.device
        )
        self.target_network.load_state_dict(self.network.state_dict())
        self.target_network.eval()

        self.optimizer = optim.Adam(self.network.parameters(), lr=alpha)
        self.loss_fn = nn.MSELoss()
        self.replay = ReplayBuffer(buffer_capacity)

    def state_from_game(self, game_state):
        vision = get_vision(game_state)
        values = encode_state_vector(vision)
        return torch.tensor(values, dtype=torch.float32, device=self.device)

    def choose_action(self, state):
        if self.learning_enabled and random.random() < self.epsilon:
            return random.choice(ACTIONS)

        with torch.no_grad():
            q_values = self.network(state.unsqueeze(0)).squeeze(0)
        best_index = int(torch.argmax(q_values).item())
        return ACTIONS[best_index]

    def update(self, state, action, reward, next_state):
        if not self.learning_enabled:
            return

        self.replay.push(state, action, reward, next_state)

        if len(self.replay) < self.batch_size:
            return

        batch = self.replay.sample(self.batch_size)
        self._train_on_batch(batch)

        self._updates_done += 1
        if self._updates_done % self.target_update_every == 0:
            self.target_network.load_state_dict(self.network.state_dict())

    def _train_on_batch(self, batch):
        states = torch.stack([s for s, a, r, ns in batch])
        action_indices = torch.tensor(
            [ACTIONS.index(a) for s, a, r, ns in batch]
        )
        rewards = torch.tensor(
            [float(r) for s, a, r, ns in batch], dtype=torch.float32
        )

        non_terminal_mask = torch.tensor(
            [ns is not None for s, a, r, ns in batch], dtype=torch.bool
        )
        non_terminal_next_states = [
            ns for s, a, r, ns in batch if ns is not None
        ]

        predicted = (
            self.network(states)
            .gather(1, action_indices.unsqueeze(1))
            .squeeze(1)
        )

        targets = rewards.clone()
        if non_terminal_next_states:
            with torch.no_grad():
                next_states_tensor = torch.stack(non_terminal_next_states)
                next_q = (
                    self.target_network(next_states_tensor).max(dim=1).values
                )
            targets[non_terminal_mask] += self.gamma * next_q

        loss = self.loss_fn(predicted, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def set_learning(self, enabled):
        self.learning_enabled = enabled
        self.network.train(mode=enabled)

    def save(self, path):
        torch.save(self.network.state_dict(), path)

    def load(self, path):
        state_dict = torch.load(path, map_location=self.device)
        self.network.load_state_dict(state_dict)
        self.target_network.load_state_dict(state_dict)
