"""Eating state: triggered by right-click menu, restores hunger."""
from config import FEED_HUNGER_BOOST, STATUS_MAX
from sprites.animation import Animation
from sprites.loader import load_sprites
from states.base_state import BaseState


class EatingState(BaseState):
    name = "eat"

    def enter(self):
        frames = load_sprites("eat")
        # Play once then return to idle
        self.anim = Animation(frames, frame_duration=0.25, loop=False)
        self.applied = False

    def update(self, dt: float):
        self.anim.update(dt)

        # Apply feeding effect after a brief delay (once per state)
        if not self.applied and self.anim.current_frame >= len(self.anim.frames) // 2:
            self.pet.status.hunger = min(
                STATUS_MAX,
                self.pet.status.hunger + FEED_HUNGER_BOOST
            )
            self.pet.status.mood = min(
                STATUS_MAX,
                self.pet.status.mood + 10
            )
            self.applied = True

        if self.anim.finished:
            from states.idle import IdleState
            self.pet.change_state(IdleState(self.pet))

    @property
    def current_image(self):
        return self.anim.current_image
