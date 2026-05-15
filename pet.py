"""Main pet controller that coordinates all systems."""
from states.idle import IdleState
from systems.interaction import InteractionHandler
from systems.reminder import ReminderSystem
from systems.status import StatusSystem

import config


class Pet:
    def __init__(self, screen_size: tuple):
        self.config = config
        self.size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # Start near center of screen
        sw, sh = screen_size
        self.position = [sw // 2 - self.size[0] // 2, sh // 2 - self.size[1] // 2]

        # Systems
        self.status = StatusSystem(config)
        self.reminder_system = ReminderSystem(config)
        self.interaction = InteractionHandler(self)

        # State
        self.state = None
        self.running = True

        # Start in idle state
        self.change_state(IdleState(self))

    def change_state(self, new_state):
        if self.state:
            self.state.exit()
        self.state = new_state
        self.state.enter()

    def update(self, dt: float):
        self.status.update(dt)
        self.state.update(dt)
        self.reminder_system.update()

    def handle_event(self, event) -> bool:
        return self.interaction.handle_event(event)

    def draw(self, surface):
        """Draw the pet and any overlays onto the given surface."""
        # Fill with transparent
        surface.fill((0, 0, 0, 0))

        # Draw pet sprite
        if self.state and self.state.current_image:
            img = self.state.current_image
            surface.blit(img, (0, 0))

        # Draw speech bubble
        x, y = self.position
        self.reminder_system.draw_bubble(surface, x, y, self.size[1])
