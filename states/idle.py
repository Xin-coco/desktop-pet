"""Idle state: the pet stays in place with breathing/blinking animation."""
import random

from config import WALK_INTERVAL_MIN, WALK_INTERVAL_MAX
from sprites.animation import Animation
from sprites.loader import load_sprites
from states.base_state import BaseState


class IdleState(BaseState):
    name = "idle"

    def enter(self):
        frames = load_sprites("idle")
        self.anim = Animation(frames, frame_duration=0.5, loop=True)
        self.walk_timer = random.uniform(WALK_INTERVAL_MIN, WALK_INTERVAL_MAX)

    def update(self, dt: float):
        self.anim.update(dt)

        # Randomly decide to walk
        self.walk_timer -= dt
        if self.walk_timer <= 0:
            from states.walking import WalkingState
            self.pet.change_state(WalkingState(self.pet))

        # Auto-sleep if energy is critically low
        if self.pet.status.energy <= self.pet.config.AUTO_SLEEP_THRESHOLD:
            from states.sleeping import SleepingState
            self.pet.change_state(SleepingState(self.pet))

    def handle_click(self, pos) -> bool:
        # Pet the pet — mood boost
        self.pet.status.mood = min(
            self.pet.config.STATUS_MAX,
            self.pet.status.mood + self.pet.config.CLICK_MOOD_BOOST
        )
        return True

    @property
    def current_image(self):
        return self.anim.current_image
