"""Walking state: the pet moves to a random position on screen."""
import math
import random

import pygame

from config import WALK_SPEED, WALK_DURATION_MIN, WALK_DURATION_MAX
from sprites.animation import Animation
from sprites.loader import load_sprites
from states.base_state import BaseState


class WalkingState(BaseState):
    name = "walk"

    def enter(self):
        frames = load_sprites("walk")
        self.anim = Animation(frames, frame_duration=0.2, loop=True)

        # Pick a random target position on screen
        screen_w, screen_h = pygame.display.get_desktop_sizes()[0]
        margin = 100
        self.target_x = random.randint(margin, screen_w - margin)
        self.target_y = random.randint(margin, screen_h - margin - 200)

        start_x, start_y = self.pet.position
        dx = self.target_x - start_x
        dy = self.target_y - start_y
        dist = math.hypot(dx, dy)

        self.duration = random.uniform(WALK_DURATION_MIN, WALK_DURATION_MAX)
        self.speed = WALK_SPEED

        if dist > 0:
            self.dir_x = dx / dist
            self.dir_y = dy / dist
        else:
            self.dir_x = 0
            self.dir_y = 0
            self.duration = 0

        self.elapsed = 0.0

    def update(self, dt: float):
        self.anim.update(dt)
        self.elapsed += dt

        if self.elapsed >= self.duration:
            from states.idle import IdleState
            self.pet.change_state(IdleState(self.pet))
            return

        # Move pet
        x, y = self.pet.position
        x += self.dir_x * self.speed * dt
        y += self.dir_y * self.speed * dt
        self.pet.position = (x, y)

    @property
    def current_image(self):
        return self.anim.current_image
