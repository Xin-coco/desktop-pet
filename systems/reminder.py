"""Reminder system with speech bubble display."""
import time

import pygame

from config import BUBBLE_BG, BUBBLE_TEXT, BUBBLE_SHOW_SECONDS


class Reminder:
    def __init__(self, message: str, trigger_time: float):
        self.message = message
        self.trigger_time = trigger_time
        self.triggered = False
        self.display_until = 0.0


class ReminderSystem:
    def __init__(self, config):
        self.config = config
        self.reminders: list[Reminder] = []
        self.active_bubble = None  # (message, display_until)
        self._font = None

    def add_reminder(self, message: str, delay_seconds: float):
        """Schedule a new reminder."""
        trigger = time.time() + delay_seconds
        self.reminders.append(Reminder(message, trigger))

    def update(self):
        """Check for due reminders and show bubble."""
        now = time.time()

        for r in self.reminders:
            if not r.triggered and now >= r.trigger_time:
                r.triggered = True
                r.display_until = now + BUBBLE_SHOW_SECONDS
                self.active_bubble = r

        # Clear expired bubble
        if self.active_bubble and now >= self.active_bubble.display_until:
            self.active_bubble = None

        # Clean up old reminders
        self.reminders = [
            r for r in self.reminders
            if not r.triggered or now < r.display_until
        ]

    @property
    def has_bubble(self) -> bool:
        return self.active_bubble is not None

    @property
    def bubble_message(self) -> str:
        if self.active_bubble:
            return self.active_bubble.message
        return ""

    def draw_bubble(self, surface, pet_x, pet_y, pet_h):
        """Draw a speech bubble above the pet."""
        if not self.has_bubble:
            return

        if self._font is None:
            self._font = pygame.font.Font(None, 22)

        message = self.bubble_message
        text_surf = self._font.render(message, True, BUBBLE_TEXT)
        text_rect = text_surf.get_rect()

        # Bubble dimensions
        padding = 12
        bubble_w = text_rect.width + padding * 2
        bubble_h = text_rect.height + padding * 2

        # Position above the pet
        bubble_x = pet_x + pet_h // 2 - bubble_w // 2
        bubble_y = pet_y - bubble_h - 10

        # Ensure bubble stays on screen
        screen_w = surface.get_width()
        if bubble_x < 5:
            bubble_x = 5
        elif bubble_x + bubble_w > screen_w - 5:
            bubble_x = screen_w - bubble_w - 5
        if bubble_y < 5:
            bubble_y = pet_y + pet_h + 10  # Show below if no room above

        # Draw bubble background
        bubble_surf = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
        pygame.draw.rect(
            bubble_surf, BUBBLE_BG,
            bubble_surf.get_rect(), border_radius=10
        )
        # Small triangle pointer
        tri_points = [
            (bubble_w // 2 - 8, bubble_h),
            (bubble_w // 2 + 8, bubble_h),
            (bubble_w // 2, bubble_h + 8),
        ]
        pygame.draw.polygon(bubble_surf, BUBBLE_BG, tri_points)

        surface.blit(bubble_surf, (bubble_x, bubble_y))

        # Draw text
        text_x = bubble_x + padding
        text_y = bubble_y + padding
        surface.blit(text_surf, (text_x, text_y))
