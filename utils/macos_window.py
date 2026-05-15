"""macOS-specific window management for transparent floating window."""
import ctypes
import os
import platform


def make_window_transparent(pygame_window):
    """Make a Pygame window transparent and always-on-top on macOS.

    Uses ctypes to call AppKit APIs. Falls back gracefully on non-macOS.
    """
    if platform.system() != "Darwin":
        return False

    try:
        # Get the SDL window pointer from Pygame
        sdl = ctypes.cdll.LoadLibrary("libSDL2-2.0.dylib")
        sdl.SDL_GetWindowWMInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        sdl.SDL_GetWindowWMInfo.restype = ctypes.c_int

        # Get NSWindow from SDL
        wm_info = ctypes.create_string_buffer(256)
        sdl.SDL_GetWindowWMInfo(pygame_window, ctypes.byref(wm_info))

        # Use objc to set window properties
        objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.A.dylib")

        # Load AppKit
        foundation = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/Foundation.framework/Foundation"
        )
        app_kit = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/AppKit.framework/AppKit"
        )

        objc.objc_getClass.restype = ctypes.c_void_p
        objc.objc_msgSend.restype = ctypes.c_void_p
        objc.sel_registerName.restype = ctypes.c_void_p

        # Get the Cocoa window from SDL
        NSWindow = objc.objc_getClass(b"NSWindow")
        NSColor = objc.objc_getClass(b"NSColor")

        # Get the key window (our SDL window)
        sel = objc.sel_registerName(b"sharedApplication")
        NSApp = objc.objc_msgSend(
            objc.objc_getClass(b"NSApplication"), sel
        )
        sel = objc.sel_registerName(b"keyWindow")
        nswindow = objc.objc_msgSend(NSApp, sel)

        if nswindow:
            # Set transparent background
            sel = objc.sel_registerName(b"setOpaque:")
            objc.objc_msgSend(nswindow, sel, ctypes.c_bool(False))

            sel = objc.sel_registerName(b"clearColor")
            clear_color = objc.objc_msgSend(NSColor, sel)
            sel = objc.sel_registerName(b"setBackgroundColor:")
            objc.objc_msgSend(nswindow, sel, clear_color)

            # Set always on top
            sel = objc.sel_registerName(b"setLevel:")
            kCGFloatingWindowLevel = 5
            objc.objc_msgSend(
                nswindow, sel, ctypes.c_int(kCGFloatingWindowLevel)
            )

            # Allow the window to be moved by dragging
            sel = objc.sel_registerName(b"setMovableByWindowBackground:")
            objc.objc_msgSend(nswindow, sel, ctypes.c_bool(True))

            return True

        return False

    except Exception:
        return False


def set_ignore_mouse(pygame_window, ignore: bool):
    """Toggle whether mouse events pass through the window."""
    if platform.system() != "Darwin":
        return

    try:
        objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.A.dylib")
        sel_app = objc.sel_registerName(b"sharedApplication")
        NSApp_cls = objc.objc_getClass(b"NSApplication")
        objc.objc_msgSend.restype = ctypes.c_void_p
        NSApp = objc.objc_msgSend(NSApp_cls, sel_app)

        sel = objc.sel_registerName(b"keyWindow")
        nswindow = objc.objc_msgSend(NSApp, sel)

        if nswindow:
            # Get the content view and add a non-interactive overlay when ignoring
            sel = objc.sel_registerName(b"setIgnoresMouseEvents:")
            objc.objc_msgSend(nswindow, sel, ctypes.c_bool(ignore))
    except Exception:
        pass
