"""Mouse interaction handler for click, drag, and right-click."""
import pygame


class InteractionHandler:
    def __init__(self, pet):
        self.pet = pet
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Returns True if consumed."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._on_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._on_mouse_up(event)
        elif event.type == pygame.MOUSEMOTION:
            return self._on_mouse_move(event)
        return False

    def _on_mouse_down(self, event) -> bool:
        if not self._hit_test(event.pos):
            return False

        if event.button == 1:  # Left click
            self.dragging = True
            px, py = self.pet.position
            mx, my = event.pos
            self.drag_offset_x = px - mx
            self.drag_offset_y = py - my
            return True

        elif event.button == 3:  # Right click
            from systems.menu import show_context_menu
            show_context_menu(self.pet, event.pos)
            return True

        return False

    def _on_mouse_up(self, event) -> bool:
        if event.button == 1:
            if self.dragging:
                # If barely moved, treat as click (pet)
                dx = abs(event.pos[0] - (
                    self.pet.position[0] - self.drag_offset_x
                ))
                dy = abs(event.pos[1] - (
                    self.pet.position[1] - self.drag_offset_y
                ))
                self.dragging = False

                if dx < 5 and dy < 5:
                    # It was a click, not a drag
                    return self.pet.state.handle_click(event.pos)

            self.dragging = False
            return True
        return False

    def _on_mouse_move(self, event) -> bool:
        if self.dragging:
            mx, my = event.pos
            self.pet.position = (
                mx + self.drag_offset_x,
                my + self.drag_offset_y,
            )
            return True
        return False

    def _hit_test(self, pos) -> bool:
        """Check if a mouse position hits the pet's bounding box."""
        px, py = self.pet.position
        w, h = self.pet.size
        return px <= pos[0] <= px + w and py <= pos[1] <= py + h
