#!/usr/bin/env python3
"""
sleepscreen.py — Borderlands-themed dim sleep screen with spinning yin-yang and animated arcs.
Exits on any keypress or mouse movement.
"""

import pygame
import sys
import math
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
BG_COLOR        = (3, 6, 10)
TIME_COLOR      = (225, 240, 255)
DATE_COLOR      = (120, 180, 210)
AMPM_COLOR      = (0, 212, 232)

YIN_COLOR       = (15, 20, 30)
YANG_COLOR      = (210, 240, 255)
CYAN            = (0, 215, 255)

MOUSE_THRESHOLD = 5
IDLE_GRACE_MS   = 800
# ─────────────────────────────────────────────────────────────────────────────

ARC_DEFS = [
    # (radius_pct, start_angle, span_pct, speed, alpha, width_pct)
    (0.265, 0.0,  0.28,  0.002, 0.65, 0.006),
    (0.265, 2.1,  0.08,  0.002, 0.35, 0.006),
    (0.265, 4.5,  0.15,  0.002, 0.50, 0.006),
    (0.290, 1.2,  0.22, -0.0015,0.40, 0.004),
    (0.290, 3.8,  0.08, -0.0015,0.22, 0.004),
    (0.290, 5.5,  0.25, -0.0015,0.32, 0.004),
    (0.315, 0.5,  0.14,  0.001, 0.25, 0.003),
    (0.315, 2.8,  0.06,  0.001, 0.15, 0.003),
    (0.315, 4.2,  0.18,  0.001, 0.20, 0.003),
]


def load_font(size, bold=False):
    for name in ["DejaVu Sans", "Liberation Sans", "Ubuntu", "FreeSans", ""]:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, size)


def draw_arc(surface, cx, cy, radius, start_angle, end_angle, color, width):
    steps = max(60, int((end_angle - start_angle) * radius))
    prev = None
    for i in range(steps + 1):
        t = start_angle + (end_angle - start_angle) * i / steps
        x = int(cx + radius * math.cos(t))
        y = int(cy + radius * math.sin(t))
        if prev:
            pygame.draw.line(surface, color, prev, (x, y), width)
        prev = (x, y)


def cyan_color(alpha):
    return (0, int(215 * alpha), int(255 * alpha), int(alpha * 255))


def draw_yinyang(surface, cx, cy, r, rotation):
    # Draw on a temp surface then rotate and blit
    size = r * 2 + 60  # extra room for glow rings
    yy = pygame.Surface((size, size), pygame.SRCALPHA)
    c = size // 2  # center of temp surface

    # ── Layer 1: full circle YANG (light) ──
    pygame.draw.circle(yy, YANG_COLOR, (c, c), r)

    # ── Layer 2: right half YIN (dark) using clip ──
    clip_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(clip_surf, YIN_COLOR, (c, c), r)
    # Mask out the left half — paint left half transparent
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (0, 0, 0, 255), (0, 0, c, size))
    clip_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    yy.blit(clip_surf, (0, 0))

    # ── Layer 3: top small circle YIN (dark bulges into light side) ──
    pygame.draw.circle(yy, YIN_COLOR, (c, c - r // 2), r // 2)

    # ── Layer 4: bottom small circle YANG (light bulges into dark side) ──
    pygame.draw.circle(yy, YANG_COLOR, (c, c + r // 2), r // 2)

    # ── Layer 5: WHITE dot in dark half (top) ──
    pygame.draw.circle(yy, YANG_COLOR, (c, c - r // 2), r // 5)

    # ── Layer 6: BLACK dot in light half (bottom) ──
    pygame.draw.circle(yy, YIN_COLOR, (c, c + r // 2), r // 5)

    # ── Outer border ──
    pygame.draw.circle(yy, CYAN, (c, c), r, 3)

    # ── S-curve divider (drawn as two arcs) ──
    draw_arc(yy, c, c - r // 2, r // 2,
             -math.pi / 2, math.pi / 2, CYAN, 2)
    draw_arc(yy, c, c + r // 2, r // 2,
             math.pi / 2, math.pi * 1.5, CYAN, 2)

    # ── Glow rings ──
    for glow, alpha in [(r + 8, 60), (r + 16, 35), (r + 24, 18)]:
        pygame.draw.circle(yy, (0, 212, 232, alpha), (c, c), glow, 2)

    # ── Dot outlines ──
    pygame.draw.circle(yy, CYAN, (c, c - r // 2), r // 5, 1)
    pygame.draw.circle(yy, CYAN, (c, c + r // 2), r // 5, 1)

    # ── Rotate and blit ──
    rotated = pygame.transform.rotozoom(yy, math.degrees(rotation), 1.0)
    rect = rotated.get_rect(center=(cx, cy))
    surface.blit(rotated, rect)


def run():
    pygame.init()

    info = pygame.display.Info()
    W, H = info.current_w, info.current_h

    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption("sleepscreen")
    pygame.mouse.set_visible(False)
    tick_clock = pygame.time.Clock()

    vault_r = int(min(W, H) * 0.18)
    cx, cy  = W // 2, H // 2

    # Build arc state
    arcs = []
    for r_pct, start, span, speed, alpha, w_pct in ARC_DEFS:
        arcs.append({
            "r":     int(min(W, H) * r_pct),
            "angle": start,
            "span":  span * math.pi * 2,
            "speed": speed,
            "alpha": alpha,
            "width": max(1, int(min(W, H) * w_pct)),
        })

    font_time = load_font(int(H * 0.11))
    font_ampm = load_font(int(H * 0.038))
    font_date = load_font(int(H * 0.030))

    start_ms    = pygame.time.get_ticks()
    start_mouse = pygame.mouse.get_pos()
    overlay     = pygame.Surface((W, H), pygame.SRCALPHA)
    rotation    = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit(); sys.exit()

        elapsed = pygame.time.get_ticks() - start_ms
        if elapsed > IDLE_GRACE_MS:
            mx, my = pygame.mouse.get_pos()
            sx, sy = start_mouse
            if abs(mx - sx) > MOUSE_THRESHOLD or abs(my - sy) > MOUSE_THRESHOLD:
                pygame.quit(); sys.exit()

        # ── Draw ───────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        overlay.fill((0, 0, 0, 0))

        # Center glow
        glow_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        glow_r = int(vault_r * 1.35)
        for gr, ga in [(glow_r, 18), (int(glow_r*0.7), 12), (int(glow_r*0.4), 8)]:
            pygame.draw.circle(glow_surf, (0, 212, 232, ga), (cx, cy), gr)
        overlay.blit(glow_surf, (0, 0))

        # Arcs
        for arc in arcs:
            arc["angle"] += arc["speed"]
            color = (0, int(215 * arc["alpha"]), 255, int(arc["alpha"] * 255))
            draw_arc(overlay, cx, cy,
                     arc["r"],
                     arc["angle"],
                     arc["angle"] + arc["span"],
                     color,
                     arc["width"])

        # Yin-yang
        rotation -= 0.002   # clockwise
        draw_yinyang(overlay, cx, cy, vault_r, rotation)

        screen.blit(overlay, (0, 0))

        # Clock
        now      = datetime.now()
        hour_str = now.strftime("%-I")
        min_str  = now.strftime("%M")
        ampm_str = now.strftime("%p")
        date_str = now.strftime("%A, %B %-d")
        time_str = f"{hour_str}:{min_str}"

        pad_x, pad_y = int(W * 0.03), int(H * 0.04)

        t_surf = font_time.render(time_str, True, TIME_COLOR)
        screen.blit(t_surf, (pad_x, pad_y))

        a_surf = font_ampm.render(ampm_str, True, AMPM_COLOR)
        a_x    = pad_x + t_surf.get_width() + int(W * 0.006)
        a_y    = pad_y + t_surf.get_height() - a_surf.get_height() - int(H * 0.01)
        screen.blit(a_surf, (a_x, a_y))

        d_surf = font_date.render(date_str, True, DATE_COLOR)
        d_y    = pad_y + t_surf.get_height() + int(H * 0.005)
        screen.blit(d_surf, (pad_x, d_y))

        pygame.display.flip()
        tick_clock.tick(30)


if __name__ == "__main__":
    run()