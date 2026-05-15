"""Desktop Pet - Main entry point."""
import ctypes
import sys

import pygame

from config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from pet import Pet
from utils.macos_window import make_window_transparent


def _get_sdl_window_pos(hwnd):
    """Get SDL window position via ctypes."""
    try:
        sdl = ctypes.cdll.LoadLibrary("libSDL2-2.0.dylib")
        sdl.SDL_GetWindowPosition.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        x = ctypes.c_int()
        y = ctypes.c_int()
        sdl.SDL_GetWindowPosition(hwnd, ctypes.byref(x), ctypes.byref(y))
        return x.value, y.value
    except Exception:
        return 0, 0


def _set_sdl_window_pos(hwnd, x: int, y: int):
    """Set SDL window position via ctypes."""
    try:
        sdl = ctypes.cdll.LoadLibrary("libSDL2-2.0.dylib")
        sdl.SDL_SetWindowPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        sdl.SDL_SetWindowPosition(hwnd, x, y)
    except Exception:
        pass


def main():
    pygame.init()

    # Small borderless window just for the pet
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.NOFRAME,
    )
    pygame.display.set_caption("Desktop Pet")

    # Get the SDL window handle
    hwnd = pygame.display.get_wm_info()["window"]

    # Make it transparent and always-on-top on macOS
    make_window_transparent(hwnd)

    # Use a rendering surface with alpha
    pet_surface = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
    )

    # Get screen size for initial positioning
    screen_w, screen_h = pygame.display.get_desktop_sizes()[0]

    pet = Pet((screen_w, screen_h))
    clock = pygame.time.Clock()

    # Set initial window position
    _set_sdl_window_pos(hwnd, int(pet.position[0]), int(pet.position[1]))

    while pet.running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pet.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (
                    event.key == pygame.K_q
                    and event.mod & pygame.KMOD_META
                ):
                    pet.running = False
            else:
                pet.handle_event(event)

        pet.update(dt)

        # Update window position to follow pet
        _set_sdl_window_pos(
            hwnd, int(pet.position[0]), int(pet.position[1])
        )

        # Render
        screen.fill((0, 0, 0))
        screen.set_colorkey((0, 0, 0))

        pet.draw(pet_surface)
        screen.blit(pet_surface, (0, 0))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
