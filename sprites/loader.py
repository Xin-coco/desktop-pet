"""Sprite loader supporting sequence frames from disk or generated fallback."""
import os
import re

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT


def _try_load_sprites(state_name: str) -> list[pygame.Surface]:
    """Load PNG sequence frames from assets/sprites/<state_name>/."""
    sprite_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets", "sprites", state_name
    )
    if not os.path.isdir(sprite_dir):
        return []

    files = []
    for f in os.listdir(sprite_dir):
        if f.lower().endswith(".png"):
            # Extract number for sorting if present
            match = re.search(r"(\d+)", f)
            order = int(match.group(1)) if match else 0
            files.append((order, os.path.join(sprite_dir, f)))

    files.sort(key=lambda x: x[0])
    frames = []
    for _, path in files:
        try:
            img = pygame.image.load(path).convert_alpha()
            # Scale to window size while maintaining aspect ratio
            img = pygame.transform.scale(
                img,
                (WINDOW_WIDTH, WINDOW_HEIGHT),
            )
            frames.append(img)
        except pygame.error:
            continue

    return frames


def _generate_fallback_sprites(state_name: str) -> list[pygame.Surface]:
    """Generate simple colored shape sprites as fallback when no images found."""
    frames = []
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    cx, cy = size[0] // 2, size[1] // 2
    r = min(cx, cy) - 10

    colors = {
        "idle":   (255, 180, 100),
        "walk":   (255, 200, 120),
        "sleep":  (200, 200, 240),
        "eat":    (255, 220, 150),
        "play":   (255, 160, 200),
    }
    base_color = colors.get(state_name, (200, 200, 200))

    if state_name == "idle":
        # Breathing effect: two frames with slightly different sizes
        for scale in [1.0, 0.95]:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            rr = int(r * scale)
            # Body
            pygame.draw.circle(surf, base_color, (cx, cy), rr)
            # Eyes
            eye_y = cy - rr // 4
            for ex in (cx - rr // 3, cx + rr // 3):
                pygame.draw.circle(surf, (255, 255, 255), (ex, eye_y), rr // 5)
                pygame.draw.circle(surf, (30, 30, 30), (ex, eye_y), rr // 10)
            # Mouth
            mouth_y = cy + rr // 4
            pygame.draw.arc(
                surf, (30, 30, 30),
                (cx - rr // 4, mouth_y - rr // 6, rr // 2, rr // 3),
                0, 3.14, 2
            )
            frames.append(surf)
    elif state_name == "walk":
        for offset in [-3, 3]:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            ox = cx + offset
            # Body
            pygame.draw.circle(surf, base_color, (ox, cy), r)
            # Eyes
            eye_y = cy - r // 4
            for ex in (ox - r // 3, ox + r // 3):
                pygame.draw.circle(surf, (255, 255, 255), (ex, eye_y), r // 5)
                pygame.draw.circle(surf, (30, 30, 30), (ex, eye_y), r // 10)
            # Feet
            foot_y = cy + r
            for fx in (ox - r // 3, ox + r // 3):
                pygame.draw.ellipse(
                    surf, base_color,
                    (fx - r // 6, foot_y - r // 2, r // 3, r // 2)
                )
            # Mouth
            pygame.draw.arc(
                surf, (30, 30, 30),
                (ox - r // 4, cy + r // 4 - r // 6, r // 2, r // 3),
                0, 3.14, 2
            )
            frames.append(surf)
    elif state_name == "sleep":
        for z_idx in range(2):
            surf = pygame.Surface(size, pygame.SRCALPHA)
            # Body (slightly squished)
            pygame.draw.ellipse(
                surf, base_color,
                (cx - r, cy - r // 2, r * 2, r)
            )
            # Closed eyes (lines)
            for ex in (cx - r // 3, cx + r // 3):
                pygame.draw.line(
                    surf, (30, 30, 30),
                    (ex - r // 5, cy - r // 6),
                    (ex + r // 5, cy - r // 6),
                    2
                )
            # Zzz
            zx, zy = cx + r, cy - r
            z_text = ["z", "zz"][z_idx]
            font = pygame.font.Font(None, 30)
            z_surf = font.render(z_text, True, (100, 100, 200))
            surf.blit(z_surf, (zx, zy - z_idx * 15))
            frames.append(surf)
    elif state_name == "eat":
        for mouth_open in [False, True]:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.circle(surf, base_color, (cx, cy), r)
            eye_y = cy - r // 4
            for ex in (cx - r // 3, cx + r // 3):
                # Happy squinty eyes
                pygame.draw.line(
                    surf, (30, 30, 30),
                    (ex - r // 5, eye_y),
                    (ex + r // 5, eye_y),
                    3
                )
            # Mouth
            mouth_y = cy + r // 4
            if mouth_open:
                pygame.draw.ellipse(
                    surf, (80, 40, 30),
                    (cx - r // 4, mouth_y - r // 6, r // 2, r // 3)
                )
            else:
                pygame.draw.arc(
                    surf, (30, 30, 30),
                    (cx - r // 4, mouth_y - r // 6, r // 2, r // 3),
                    0, 3.14, 2
                )
            frames.append(surf)
    elif state_name == "play":
        for bounce in [0, -20]:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            by = cy + bounce
            pygame.draw.circle(surf, base_color, (cx, by), r)
            # Happy wide eyes
            eye_y = by - r // 4
            for ex in (cx - r // 3, cx + r // 3):
                pygame.draw.circle(
                    surf, (255, 255, 255), (ex, eye_y), r // 4
                )
                pygame.draw.circle(
                    surf, (30, 30, 30), (ex, eye_y), r // 8
                )
            # Big smile
            mouth_y = by + r // 4
            pygame.draw.arc(
                surf, (30, 30, 30),
                (cx - r // 3, mouth_y - r // 6, r * 2 // 3, r // 2),
                0.2, 2.94, 2
            )
            # Sparkles
            sparkle_positions = [(cx + r, by - r // 2), (cx - r - 10, by - r // 3)]
            for sx, sy in sparkle_positions:
                color = (255, 255, 100) if bounce == 0 else (255, 200, 255)
                pygame.draw.circle(surf, color, (sx, sy), 5)
            frames.append(surf)

    return frames


def load_sprites(state_name: str) -> list[pygame.Surface]:
    """Load sprite frames for a state, falling back to generated shapes."""
    frames = _try_load_sprites(state_name)
    if not frames:
        frames = _generate_fallback_sprites(state_name)
    return frames
