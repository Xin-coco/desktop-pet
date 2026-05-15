"""Playing state: triggered by right-click menu, boosts mood."""
from config import PLAY_MOOD_BOOST, PLAY_ENERGY_COST, STATUS_MAX, STATUS_MIN
from sprites.animation import Animation
from sprites.loader import load_sprites
from states.base_state import BaseState


class PlayingState(BaseState):
    name = "play"

    def enter(self):
        frames = load_sprites("play")
        self.anim = Animation(frames, frame_duration=0.2, loop=False)
        self.applied = False

    def update(self, dt: float):
        self.anim.update(dt)

        if not self.applied and self.anim.current_frame >= len(self.anim.frames) // 2:
            self.pet.status.mood = min(
                STATUS_MAX,
                self.pet.status.mood + PLAY_MOOD_BOOST
            )
            self.pet.status.energy = max(
                STATUS_MIN,
                self.pet.status.energy - PLAY_ENERGY_COST
            )
            self.applied = True

        if self.anim.finished:
            from states.idle import IdleState
            self.pet.change_state(IdleState(self.pet))

    @property
    def current_image(self):
        return self.anim.current_image
