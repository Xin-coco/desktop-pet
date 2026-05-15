"""Sleeping state: the pet rests and recovers energy."""
from config import ENERGY_RECOVER, STATUS_MAX
from sprites.animation import Animation
from sprites.loader import load_sprites
from states.base_state import BaseState


class SleepingState(BaseState):
    name = "sleep"

    def enter(self):
        frames = load_sprites("sleep")
        self.anim = Animation(frames, frame_duration=0.8, loop=True)

    def update(self, dt: float):
        self.anim.update(dt)
        # Recover energy
        self.pet.status.energy = min(
            STATUS_MAX,
            self.pet.status.energy + ENERGY_RECOVER * dt
        )

    def exit(self):
        pass

    def handle_click(self, pos) -> bool:
        # Click to wake up
        from states.idle import IdleState
        self.pet.change_state(IdleState(self.pet))
        return True

    @property
    def current_image(self):
        return self.anim.current_image
