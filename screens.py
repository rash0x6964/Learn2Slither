import os
import theme
import pygame
from widgets import Button, SelectList, Stepper, Toggle

MENU_WINDOW_SIZE = (480, 480)
MODELS_DIR = "models"


def _models_available():
    if not os.path.isdir(MODELS_DIR):
        return []
    return sorted(f for f in os.listdir(MODELS_DIR) if f.endswith(".pt"))


def show_lobby(window, clock):
    result = {"value": None}
    cx = MENU_WINDOW_SIZE[0] // 2

    start_button = Button(
        (cx - 100, 260, 200, 48),
        "START",
        lambda: result.__setitem__("value", "start"),
    )
    quit_button = Button(
        (cx - 100, 320, 200, 48),
        "QUIT",
        lambda: result.__setitem__("value", "quit"),
    )
    widgets = [start_button, quit_button]

    while result["value"] is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            for widget in widgets:
                widget.handle_event(event)

        window.fill(theme.DARK)
        theme.draw_text(
            window,
            "LEARN2SLITHER",
            (cx, 140),
            size=38,
            color=theme.GOOD,
            center=True,
        )
        theme.draw_text(
            window,
            "a snake that learns through trial and error",
            (cx, 185),
            size=13,
            color=theme.MUTED,
            center=True,
        )
        for widget in widgets:
            widget.draw(window)
        pygame.display.flip()
        clock.tick(60)

    return result["value"]


def show_config(window, clock, args):
    result = {"value": None}

    sessions_stepper = Stepper(
        (40, 110, 400, 32), "Sessions", args.sessions, 10, 1, 100000, "{:.0f}"
    )
    speed_stepper = Stepper(
        (40, 160, 400, 32), "Speed (moves/sec)", args.speed, 1, 1, 60, "{:.0f}"
    )
    board_stepper = Stepper(
        (40, 210, 400, 32), "Board size", args.board_size, 1, 5, 30, "{:.0f}"
    )
    dontlearn_toggle = Toggle(
        (40, 260, 90, 28), "Don't learn (exploit only)", args.dontlearn
    )

    models = _models_available()
    initial_index = 0
    if args.load:
        base = os.path.basename(args.load)
        if base in models:
            initial_index = models.index(base) + 1
    load_select = SelectList(
        (40, 330, 400, 120), ["(none)"] + models, initial_index
    )

    def start():
        selected = load_select.selected
        load_path = args.load
        if selected and selected != "(none)":
            load_path = os.path.join(MODELS_DIR, selected)
        elif selected == "(none)":
            load_path = None
        result["value"] = {
            "sessions": int(sessions_stepper.value),
            "speed": speed_stepper.value,
            "board_size": int(board_stepper.value),
            "dontlearn": dontlearn_toggle.value,
            "load_path": load_path,
            "save_path": args.save,
            "max_steps": args.max_steps,
        }

    def back():
        result["value"] = "back"

    start_button = Button((40, 460, 180, 40), "START", start)
    back_button = Button((240, 460, 180, 40), "BACK", back)

    widgets = [
        sessions_stepper,
        speed_stepper,
        board_stepper,
        dontlearn_toggle,
        load_select,
        start_button,
        back_button,
    ]

    while result["value"] is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            for widget in widgets:
                widget.handle_event(event)

        window.fill(theme.DARK)
        theme.draw_text(
            window, "CONFIGURATION", (40, 50), size=24, color=theme.INK
        )
        for widget in (
            sessions_stepper,
            speed_stepper,
            board_stepper,
            dontlearn_toggle,
        ):
            widget.draw(window)
        theme.draw_text(
            window, "Load model:", (40, 305), size=14, color=theme.INK
        )
        load_select.draw(window)
        start_button.draw(window)
        back_button.draw(window)
        pygame.display.flip()
        clock.tick(60)

    if result["value"] == "back":
        return None
    return result["value"]


def show_results(window, clock, episode_results):
    lengths = [length for length, steps in episode_results]
    durations = [steps for length, steps in episode_results]

    done = {"value": False}
    cx = MENU_WINDOW_SIZE[0] // 2
    close_button = Button(
        (cx - 100, 420, 200, 44),
        "CLOSE",
        lambda: done.__setitem__("value", True),
    )

    while not done["value"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            close_button.handle_event(event)

        window.fill(theme.DARK)
        theme.draw_text(window, "RESULTS", (40, 40), size=26, color=theme.INK)

        if lengths:
            best_length = max(lengths)
            avg_length = sum(lengths) / len(lengths)
            avg_duration = sum(durations) / len(durations)
            theme.draw_text(
                window,
                f"Sessions run: {len(lengths)}",
                (40, 100),
                size=16,
                color=theme.INK,
            )
            theme.draw_text(
                window,
                f"Best length: {best_length}",
                (40, 130),
                size=16,
                color=theme.GOOD,
            )
            theme.draw_text(
                window,
                f"Average length: {avg_length:.2f}",
                (40, 160),
                size=16,
                color=theme.INK,
            )
            theme.draw_text(
                window,
                f"Average duration: {avg_duration:.1f} steps",
                (40, 190),
                size=16,
                color=theme.INK,
            )
        else:
            theme.draw_text(
                window,
                "No sessions were completed.",
                (40, 100),
                size=16,
                color=theme.MUTED,
            )

        close_button.draw(window)
        pygame.display.flip()
        clock.tick(60)
