import pygame
import theme


class Button:
    def __init__(self, rect, label, on_click=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.enabled = enabled
        self.hovered = False

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.on_click:
                self.on_click()

    def draw(self, surface):
        if not self.enabled:
            bg, fg = theme.PANEL, theme.MUTED
        elif self.hovered:
            bg, fg = theme.ACCENT, theme.DARK
        else:
            bg, fg = theme.MUTED, theme.TEXT

        pygame.draw.rect(surface, bg, self.rect)
        theme.draw_text(
            surface,
            self.label,
            self.rect.center,
            size=16,
            color=fg,
            center=True,
        )


class Stepper:
    def __init__(
        self, rect, label, value, step, min_value, max_value, value_format="{}"
    ):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.value_format = value_format

        button_size = self.rect.height
        self.minus_button = Button(
            (
                self.rect.right - 2 * button_size - 4,
                self.rect.y,
                button_size,
                button_size,
            ),
            "-",
            self._decrement,
        )
        self.plus_button = Button(
            (
                self.rect.right - button_size,
                self.rect.y,
                button_size,
                button_size,
            ),
            "+",
            self._increment,
        )

    def _decrement(self):
        self.value = max(self.min_value, round(self.value - self.step, 4))

    def _increment(self):
        self.value = min(self.max_value, round(self.value + self.step, 4))

    def handle_event(self, event):
        self.minus_button.handle_event(event)
        self.plus_button.handle_event(event)

    def draw(self, surface):
        theme.draw_text(
            surface,
            self.label,
            (self.rect.x, self.rect.y + 4),
            size=16,
            color=theme.TEXT,
        )
        value_text = self.value_format.format(self.value)
        value_x = self.minus_button.rect.x - 70
        theme.draw_text(
            surface,
            value_text,
            (value_x, self.rect.y + 4),
            size=16,
            color=theme.TEXT,
        )
        self.minus_button.draw(surface)
        self.plus_button.draw(surface)


class Toggle:
    SWITCH_WIDTH = 70

    def __init__(self, rect, label, value=False):
        self.row_rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.switch_rect = pygame.Rect(
            self.row_rect.right - self.SWITCH_WIDTH,
            self.row_rect.y,
            self.SWITCH_WIDTH,
            self.row_rect.height,
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.switch_rect.collidepoint(event.pos):
                self.value = not self.value

    def draw(self, surface):
        theme.draw_text(
            surface,
            self.label,
            (self.row_rect.x, self.row_rect.y + 4),
            size=16,
            color=theme.TEXT,
        )
        state_text = "ON" if self.value else "OFF"
        color = theme.TEXT if self.value else theme.MUTED
        pygame.draw.rect(surface, theme.PANEL, self.switch_rect)
        pygame.draw.rect(surface, color, self.switch_rect, width=2)
        theme.draw_text(
            surface,
            state_text,
            self.switch_rect.center,
            size=14,
            color=color,
            center=True,
        )


class SelectList:
    def __init__(self, rect, options, selected_index=0, on_change=None):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected_index = selected_index if options else -1
        self.on_change = on_change
        self.row_height = 28

    @property
    def selected(self):
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                row = (event.pos[1] - self.rect.y) // self.row_height
                if 0 <= row < len(self.options):
                    self.selected_index = row
                    if self.on_change:
                        self.on_change(self.options[row])

    def draw(self, surface):
        pygame.draw.rect(surface, theme.PANEL, self.rect)
        if not self.options:
            theme.draw_text(
                surface,
                "(none found)",
                (self.rect.x + 8, self.rect.y + 8),
                size=32,
                color=theme.MUTED,
            )
            return
        for i, option in enumerate(self.options):
            row_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + i * self.row_height,
                self.rect.width,
                self.row_height,
            )
            if i == self.selected_index:
                pygame.draw.rect(surface, theme.ACCENT, row_rect)
            theme.draw_text(
                surface,
                option,
                (row_rect.x + 8, row_rect.y + 6),
                size=14,
                color=theme.TEXT,
            )
