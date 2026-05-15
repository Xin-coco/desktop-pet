"""Animation controller for sprite frame sequences."""


class Animation:
    """Manages frame-by-frame sprite animation."""

    def __init__(
        self, frames: list, frame_duration: float = 0.3, loop: bool = True
    ):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.elapsed = 0.0
        self.finished = False

    @property
    def current_image(self):
        """Get the current frame surface, or None if no frames loaded."""
        if not self.frames:
            return None
        return self.frames[self.current_frame]

    def update(self, dt: float):
        """Advance animation by dt seconds."""
        if self.finished or not self.frames:
            return

        self.elapsed += dt
        if self.elapsed >= self.frame_duration:
            self.elapsed -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def reset(self):
        """Restart the animation from frame 0."""
        self.current_frame = 0
        self.elapsed = 0.0
        self.finished = False
