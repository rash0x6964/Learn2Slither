import argparse
import sys

import pygame

from environment.game_state import GameState
from environment.renderer import Renderer
from interpreter import print_vision
from agent.agent import QLearningAgent
from agent.action import action_to_vector
from agent.rewards import compute_reward


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="snake", description="Learn2Slither")

    parser.add_argument(
        "-sessions",
        type=int,
        default=1,
        help="number of training sessions to run",
    )
    parser.add_argument(
        "-save",
        type=str,
        default=None,
        help="path to save the trained model to, after all sessions",
    )
    parser.add_argument(
        "-load",
        type=str,
        default=None,
        help="path to load a previously trained model from",
    )
    parser.add_argument(
        "-visual",
        choices=["on", "off"],
        default="on",
        help="show the graphical board + terminal vision (on), "
        "or run headless with only Game-over summaries (off)",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="exploitation only: ignore rewards, never update the model",
    )
    parser.add_argument(
        "-step-by-step",
        dest="step_by_step",
        action="store_true",
        help="pause after every move; advance with SPACE in the game window "
        "(only meaningful together with -visual on)",
    )
    parser.add_argument(
        "-speed",
        type=float,
        default=10.0,
        help="moves per second in visual mode (ignored in step-by-step mode)",
    )
    parser.add_argument(
        "-board-size", type=int, default=10, help="board width/height in cells"
    )
    return parser.parse_args(argv)


def _wait_for_step():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                return True


def _pump_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True


def run(args):
    game_state = GameState(args.board_size)
    agent = QLearningAgent()

    if args.load:
        agent.load(args.load)
        print(f"Load trained model from {args.load}")

    if args.dontlearn:
        agent.set_learning(False)

    visual = args.visual == "on"
    renderer = Renderer(game_state) if visual else None
    clock = pygame.time.Clock() if visual else None

    keep_running = True

    for _ in range(args.sessions):
        if not keep_running:
            break

        game_state.reset()
        state = agent.state_from_game(game_state)

        while True:
            if visual:
                print_vision(game_state)

            action = agent.choose_action(state)

            if visual:
                print(action)

            info = game_state.step(action_to_vector(action))
            reward = compute_reward(info)
            next_state = (
                agent.state_from_game(game_state) if info["alive"] else None
            )
            agent.update(state, action, reward, next_state)

            if renderer:
                renderer.draw(game_state)
                if args.step_by_step:
                    keep_running = _wait_for_step()
                else:
                    keep_running = _pump_events()
                    clock.tick(args.speed)
                if not keep_running:
                    break

            if not info["alive"]:
                print(
                    f"Game over, max length = {info['max_length']}, "
                    f"max duration = {info['steps']}"
                )
                break

            state = next_state

    if renderer:
        renderer.close()

    if args.save:
        agent.save(args.save)
        print(f"Save learning state in {args.save}")


def main(argv=None):
    run(parse_args(argv))


if __name__ == "__main__":
    main(sys.argv[1:])
