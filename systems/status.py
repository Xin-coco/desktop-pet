"""Pet status system: hunger, mood, and energy that decay over time."""


class StatusSystem:
    def __init__(self, config):
        self.config = config
        self.hunger = 100.0
        self.mood = 80.0
        self.energy = 100.0

    def update(self, dt: float):
        """Decay status values over time."""
        self.hunger = max(
            self.config.STATUS_MIN,
            self.hunger - self.config.HUNGER_DECAY * dt
        )
        self.mood = max(
            self.config.STATUS_MIN,
            self.mood - self.config.MOOD_DECAY * dt
        )
        # Energy decays only when not sleeping — handled by sleeping state

    @property
    def needs_food(self):
        return self.hunger <= self.config.STATUS_LOW

    @property
    def is_unhappy(self):
        return self.mood <= self.config.STATUS_LOW

    @property
    def is_exhausted(self):
        return self.energy <= self.config.AUTO_SLEEP_THRESHOLD
