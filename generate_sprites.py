"""Process character image: remove background, pixelate, generate sprite frames."""
import math
import os
import sys

from PIL import Image, ImageDraw

SRC = os.path.expanduser("~/Downloads/图片.JPG")
OUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "sprites")

PIXEL_SIZE = 48
OUTPUT_SIZE = 200


def remove_bg(img: Image.Image) -> Image.Image:
    """Remove background using rembg (AI-based)."""
    from rembg import remove
    return remove(img)


def _make_square(img: Image.Image) -> Image.Image:
    """Center the image on a square transparent canvas."""
    max_dim = max(img.size)
    square = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    ox = (max_dim - img.width) // 2
    oy = (max_dim - img.height) // 2
    square.paste(img, (ox, oy), img)
    return square


def pixelate(img: Image.Image) -> Image.Image:
    """Downscale then upscale with nearest neighbor for pixel-art look."""
    small = img.resize((PIXEL_SIZE, PIXEL_SIZE), Image.NEAREST)
    return small.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.NEAREST)


def add_outline(img: Image.Image) -> Image.Image:
    """Add a dark outline around non-transparent pixels."""
    pixels = img.load()
    w, h = img.size
    outline = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    outline_px = outline.load()
    for y in range(h):
        for x in range(w):
            if pixels[x, y][3] > 0:
                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                    if 0 <= nx < w and 0 <= ny < h and pixels[nx, ny][3] == 0:
                        outline_px[x, y] = (0, 0, 0, 180)
                        break
    return Image.alpha_composite(img, outline)


def _make_frame(paste_img, offset=(0, 0)):
    """Create a blank OUTPUT_SIZE frame and paste img at offset."""
    frame = Image.new("RGBA", (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    frame.paste(paste_img, offset, paste_img)
    return frame


def gen_idle(base):
    """Breathing effect: 2 frames with slight scale pulse."""
    frames = []
    for scale in [1.0, 0.96]:
        nw = int(OUTPUT_SIZE * scale)
        nh = int(OUTPUT_SIZE * scale)
        scaled = base.resize((nw, nh), Image.NEAREST)
        ox = (OUTPUT_SIZE - nw) // 2
        oy = (OUTPUT_SIZE - nh) // 2
        frames.append(_make_frame(scaled, (ox, oy)))
    return frames


def gen_walk(base):
    """Horizontal sway + bob: 4 frames."""
    frames = []
    for i in range(4):
        sx = int(math.sin(i * math.pi / 2) * 8)
        sy = int(abs(math.sin(i * math.pi / 2)) * 6)
        frame = _make_frame(base, (sx, sy))
        draw = ImageDraw.Draw(frame)
        foot_y = OUTPUT_SIZE - 10
        spread = 15 + abs(sx)
        for fx in [OUTPUT_SIZE // 2 - spread, OUTPUT_SIZE // 2 + spread]:
            draw.ellipse([fx - 6, foot_y - 3, fx + 6, foot_y + 3], fill=(0, 0, 0, 80))
        frames.append(frame)
    return frames


def gen_sleep(base):
    """Squished + Zzz: 2 frames."""
    frames = []
    for i in range(2):
        squished = base.resize((OUTPUT_SIZE, int(OUTPUT_SIZE * 0.92)), Image.NEAREST)
        frame = _make_frame(squished, (0, OUTPUT_SIZE - squished.height))
        draw = ImageDraw.Draw(frame)
        draw.text((OUTPUT_SIZE - 50, 15 + i * 20), "z" * (i + 1), fill=(120, 140, 220))
        frames.append(frame)
    return frames


def gen_eat(base):
    """Vertical bob: 2 frames."""
    frames = []
    for i in range(2):
        frame = _make_frame(base, (0, -3 if i == 0 else 3))
        if i == 0:
            draw = ImageDraw.Draw(frame)
            fx, fy = OUTPUT_SIZE // 2, OUTPUT_SIZE - 30
            draw.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=(255, 200, 100))
        frames.append(frame)
    return frames


def gen_play(base):
    """Bounce + sparkles: 2 frames."""
    frames = []
    colors = [(255, 255, 100), (255, 200, 255)]
    for i in range(2):
        bounce = 0 if i == 0 else -20
        frame = _make_frame(base, (0, bounce))
        draw = ImageDraw.Draw(frame)
        for sx, sy in [(OUTPUT_SIZE - 30, 30), (20, 50), (OUTPUT_SIZE - 40, 70)][:i + 2]:
            draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=colors[i])
        frames.append(frame)
    return frames


def main():
    if not os.path.exists(SRC):
        print(f"Source image not found: {SRC}")
        print("Usage: drag your character image to ~/Downloads/图片.JPG")
        print("Or edit the SRC path in this script.")
        sys.exit(1)

    print(f"Loading: {SRC}")
    img = Image.open(SRC).convert("RGBA")
    print(f"  Original: {img.size}")

    print("Removing background (AI, may take a moment)...")
    img = remove_bg(img)
    img = _make_square(img)

    print(f"Pixelating to {PIXEL_SIZE}x{PIXEL_SIZE} -> {OUTPUT_SIZE}x{OUTPUT_SIZE}...")
    base = pixelate(img)
    base = add_outline(base)

    os.makedirs(OUT_DIR, exist_ok=True)
    base.save(os.path.join(OUT_DIR, "_preview.png"))
    print("  Preview -> assets/sprites/_preview.png")

    generators = {
        "idle":  gen_idle,
        "walk":  gen_walk,
        "sleep": gen_sleep,
        "eat":   gen_eat,
        "play":  gen_play,
    }

    for name, gen in generators.items():
        d = os.path.join(OUT_DIR, name)
        os.makedirs(d, exist_ok=True)
        for i, frame in enumerate(gen(base)):
            path = os.path.join(d, f"{name}_{i + 1:02d}.png")
            frame.save(path)
            print(f"  {path}")

    print("\nDone. Run with: python3 main.py")


if __name__ == "__main__":
    main()
