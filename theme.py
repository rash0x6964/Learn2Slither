import pygame

P0 = (7, 15, 43)
P1 = (27, 26, 85)
P2 = (83, 92, 145)
P3 = (146, 144, 195)
P4 = (225, 225, 225)

DARK = P0
PANEL = P1
MUTED = P2
ACCENT = P3
TEXT = P4

_font_cache = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        f = pygame.font.SysFont(
            "couriernew,consolas,monospace", size, bold=bold
        )
        _font_cache[key] = f
    return _font_cache[key]


def draw_text(
    surface, text, pos, size=18, color=TEXT, bold=True, center=False
):
    # antialias off: crisper/blockier
    label = font(size, bold).render(text, False, color)
    rect = label.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(label, rect)
    return rect
