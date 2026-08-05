import argparse
import sys

import pygame

import screens
from environment.game_state import GameState
from environment.renderer import Renderer
from interpreter import print_vision
from agent.agent import QLearningAgent
from agent.utils import action_to_vector, compute_reward

CELL_SIZE = 32


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
        help="show the lobby/config/board/results screens (on), "
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
    parser.add_argument(
        "-max-steps",
        type=int,
        default=2000,
        help="force a session to end as a timeout if it runs this many "
        "steps without dying -- guards against a deterministic "
        "greedy policy (e.g. -dontlearn) looping forever",
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
    clock = None
    window = None
    visual = args.visual == "on"

    if visual:
        pygame.init()
        window = pygame.display.set_mode(screens.MENU_WINDOW_SIZE)
        pygame.display.set_caption("Learn2Slither")
        clock = pygame.time.Clock()

        if screens.show_lobby(window, clock) != "start":
            pygame.quit()
            return

        config = screens.show_config(window, clock, args)
        if config is None:
            pygame.quit()
            return
    else:
        config = {
            "sessions": args.sessions,
            "speed": args.speed,
            "board_size": args.board_size,
            "dontlearn": args.dontlearn,
            "load_path": args.load,
            "save_path": args.save,
            "max_steps": args.max_steps,
        }

    game_state = GameState(config["board_size"])
    agent = QLearningAgent()

    if config["load_path"]:
        agent.load(config["load_path"])
        print(f"Load trained model from {config['load_path']}")

    if config["dontlearn"]:
        agent.set_learning(False)

    renderer = None
    if visual:
        window = pygame.display.set_mode(
            (
                config["board_size"] * CELL_SIZE,
                config["board_size"] * CELL_SIZE,
            )
        )
        renderer = Renderer(config["board_size"], cell_size=CELL_SIZE)

    keep_running = True
    episode_results = []

    for _ in range(config["sessions"]):
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

            if visual:
                renderer.draw_onto(window, game_state, top_left=(0, 0))
                pygame.display.flip()

                if args.step_by_step:
                    keep_running = _wait_for_step()
                else:
                    keep_running = _pump_events()
                    clock.tick(config["speed"])
                if not keep_running:
                    break

            if not info["alive"]:
                episode_results.append((info["max_length"], info["steps"]))
                print(
                    f"Game over, max length = {info['max_length']}, "
                    f"max duration = {info['steps']}"
                )
                break

            timed_out = game_state.steps >= config["max_steps"]
            if timed_out:
                episode_results.append((info["max_length"], info["steps"]))
                print(
                    f"Game over (timeout), max length = {info['max_length']}, "
                    f"max duration = {info['steps']}"
                )
                break

            state = next_state

    if config["save_path"]:
        agent.save(config["save_path"])
        print(f"Save learning state in {config['save_path']}")

    if visual:
        window = pygame.display.set_mode(screens.MENU_WINDOW_SIZE)
        screens.show_results(window, clock, episode_results)
        pygame.quit()


def main(argv=None):
    run(parse_args(argv))


if __name__ == "__main__":
    main(sys.argv[1:])
