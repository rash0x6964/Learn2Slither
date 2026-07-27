import pygame

# A small, cohesive "console" palette rather than arbitrary colors.
BLACK = (10, 10, 14)
DARK = (26, 28, 44)
PANEL = (38, 43, 68)
PANEL_LIGHT = (58, 65, 98)
INK = (238, 238, 246)
MUTED = (140, 146, 172)

ACCENT = (91, 206, 250)  # cyan-ish accent (buttons, highlights)
ACCENT_DARK = (48, 130, 168)
GOOD = (99, 217, 121)  # green apple / positive
BAD = (235, 82, 82)  # red apple / negative
GOLD = (247, 198, 82)  # score / highlight

SNAKE_BODY = (99, 217, 121)
SNAKE_BODY_DARK = (58, 158, 82)
SNAKE_OUTLINE = (24, 66, 34)
SNAKE_EYE = (18, 18, 22)

APPLE_GREEN = (99, 217, 121)
APPLE_GREEN_DARK = (58, 158, 82)
APPLE_RED = (231, 76, 76)
APPLE_RED_DARK = (168, 44, 44)
APPLE_HIGHLIGHT = (255, 235, 235)
APPLE_STEM = (120, 84, 48)

_font_cache = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        f = pygame.font.SysFont(
            "couriernew,consolas,monospace", size, bold=bold
        )
        _font_cache[key] = f
    return _font_cache[key]


def draw_text(surface, text, pos, size=18, color=INK, bold=True, center=False):
    # antialias off: crisper/blockier
    label = font(size, bold).render(text, False, color)
    rect = label.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(label, rect)
    return rect
