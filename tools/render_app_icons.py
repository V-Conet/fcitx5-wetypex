#!/usr/bin/env python3
"""Render the hicolor app icon set with KDE HIG colorful-icon margins.

``data/icons/source/fcitx5-wetypex.png`` is the full-bleed master artwork.
Every installed size is downsampled from it, so the whole set can be
regenerated after editing the master:

    python3 tools/render_app_icons.py

KDE's Colorful Icons guidelines use 4 px margins on the 48 px baseline, i.e.
the artwork covers 40/48 of the canvas. 32 px colorful icons are the documented
exception and use 2 px margins instead. See
https://develop.kde.org/hig/icons/colorful/

Requires Pillow (``pip install Pillow``).
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "icons" / "source" / "fcitx5-wetypex.png"
ICON_DIR = ROOT / "data" / "icons" / "hicolor"
ICON_NAME = "fcitx5-wetypex.png"
SIZES = (16, 24, 32, 48, 64, 128, 256, 1024)


# KDE HIG: 4 px at 48 px, except 2 px at 32 px.
def margin_for(size: int) -> int:
    if size == 32:
        return 2
    return max(1, round(size * 4 / 48))


def resize_rgba(image: Image.Image, size: int) -> Image.Image:
    """Resize while premultiplying alpha to avoid dark fringes."""
    return (
        image.convert("RGBa")
        .resize((size, size), Image.Resampling.LANCZOS)
        .convert("RGBA")
    )


def main() -> None:
    master = Image.open(SOURCE).convert("RGBA")

    content = master.getchannel("A").getbbox()
    if content is None:
        raise SystemExit(f"{SOURCE} is fully transparent")
    if content[2] - content[0] != content[3] - content[1]:
        raise SystemExit(f"{SOURCE} artwork is not square: {content}")
    artwork = master.crop(content)

    for size in SIZES:
        margin = margin_for(size)
        edge = size - 2 * margin
        if edge <= 0:
            raise SystemExit(f"margin {margin} leaves no room at {size}px")

        rendered = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        rendered.alpha_composite(resize_rgba(artwork, edge), (margin, margin))

        output = ICON_DIR / f"{size}x{size}" / "apps" / ICON_NAME
        output.parent.mkdir(parents=True, exist_ok=True)
        rendered.save(output, optimize=True)
        print(f"{output.relative_to(ROOT)}: {size}px, {margin}px margin")


if __name__ == "__main__":
    main()
