#!/usr/bin/env python3
"""Generate multi-resolution icon assets for OctaveLights."""

from PIL import Image, ImageDraw
import os

# Ensure assets directory exists
os.makedirs('assets', exist_ok=True)

def create_icon(size):
    """Create a piano keyboard icon at the specified size."""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate keyboard dimensions
    padding = max(1, size // 16)
    keyboard_width = size - 2 * padding
    keyboard_height = size - 2 * padding

    # Number of keys to show (depends on size)
    if size <= 16:
        num_keys = 5
    elif size <= 32:
        num_keys = 7
    else:
        num_keys = 9

    key_width = keyboard_width // num_keys
    key_height = keyboard_height

    # Draw white keys
    for i in range(num_keys):
        x = padding + i * key_width
        y = padding

        # Slightly rounded corners for visibility
        corner_radius = max(1, size // 32)

        # Draw white key background
        draw.rectangle(
            [x, y, x + key_width - 1, y + key_height - 1],
            fill='white',
            outline='black',
            width=max(1, size // 64)
        )

    # Highlight the middle key(s) with glow
    highlight_idx = num_keys // 2
    x = padding + highlight_idx * key_width
    y = padding

    # Draw highlight key with cyan/blue color and glow effect
    # Glow (outer)
    if size > 16:
        glow_color = (100, 200, 255, 120)
        corner_radius = max(1, size // 32)
        draw.rectangle(
            [x - 2, y - 2, x + key_width + 1, y + key_height + 1],
            fill=glow_color,
            outline=None
        )

    # Highlight key (inner)
    highlight_color = (50, 150, 255)
    draw.rectangle(
        [x, y, x + key_width - 1, y + key_height - 1],
        fill=highlight_color,
        outline='darkblue',
        width=max(1, size // 64)
    )

    # Add a small white dot/light on the highlight key for extra glow effect
    if size >= 32:
        dot_size = max(1, size // 24)
        dot_x = x + key_width // 2
        dot_y = y + key_height // 4
        draw.ellipse(
            [dot_x - dot_size, dot_y - dot_size, dot_x + dot_size, dot_y + dot_size],
            fill='white'
        )

    return img

def main():
    """Generate all icon sizes."""
    sizes = [16, 32, 48, 256]

    for size in sizes:
        print(f"Generating {size}x{size} icon...")
        img = create_icon(size)

        # Save as PNG
        png_path = f'assets/app-{size}.png'
        img.save(png_path, 'PNG')
        print(f"  → Saved {png_path}")

    # Create ICO file from 256x256 icon (multi-resolution)
    print("\nGenerating multi-resolution ICO file...")

    # Load all sizes
    icon_images = []
    for size in [16, 32, 48, 256]:
        img = Image.open(f'assets/app-{size}.png').convert('RGBA')
        icon_images.append(img)

    # Save as ICO (Windows will use the best resolution for each context)
    ico_path = 'assets/app.ico'
    icon_images[3].save(
        ico_path,
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (256, 256)]
    )
    print(f"  → Saved {ico_path}")

    print("\n✓ Icon generation complete!")
    print("\nGenerated files:")
    for size in sizes:
        print(f"  - assets/app-{size}.png")
    print(f"  - assets/app.ico (multi-resolution)")

if __name__ == '__main__':
    main()
