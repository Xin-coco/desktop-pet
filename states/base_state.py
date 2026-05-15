"""Base class for all pet states."""


class BaseState:
    """Abstract base for pet behavior states."""

    name = "base"

    def __init__(self, pet):
        self.pet = pet

    def enter(self):
        """Called when transitioning into this state."""
        pass

    def exit(self):
        """Called when transitioning out of this state."""
        pass

    def update(self, dt: float):
        """Update state logic. dt in seconds."""
        pass

    def handle_click(self, pos) -> bool:
        """Handle mouse click. Return True if event was consumed."""
        return False

    def handle_right_click(self, pos) -> bool:
        """Handle right click. Return True if event was consumed."""
        return False
