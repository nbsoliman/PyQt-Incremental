import os
import random
import uuid
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def generate_perlin_like_noise(width, height, scale=100, octaves=4):
    """Generates Perlin-like noise using NumPy."""
    noise = np.zeros((height, width))
    for octave in range(octaves):
        frequency = 2 ** octave
        amplitude = 0.5 ** octave
        for y in range(height):
            for x in range(width):
                noise[y, x] += (
                    amplitude
                    * random.uniform(0, 1)
                    * np.sin(2 * np.pi * frequency * x / scale)
                    * np.cos(2 * np.pi * frequency * y / scale)
                )
    # Normalize to 0-1 range
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise


def generate_realistic_planet_texture(size=2048, save_dir="assets"):
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer.")

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Generate a unique ID for the texture
    unique_id = str(uuid.uuid4())  # Create a UUID4 string
    file_path = os.path.join(save_dir, f"{unique_id}_planet_texture.jpg")

    # Create the base image
    image = Image.new("RGB", (size, size), "black")
    draw = ImageDraw.Draw(image)

    # Generate a random base color
    base_color = (
        random.randint(50, 200),  # Red
        random.randint(50, 200),  # Green
        random.randint(50, 200),  # Blue
    )

    # Generate Perlin-like noise
    noise = generate_perlin_like_noise(size, size, scale=200, octaves=4)

    # Draw base gradient with Perlin-like noise
    for y in range(size):
        for x in range(size):
            intensity = noise[y, x]
            r = int(base_color[0] * intensity)
            g = int(base_color[1] * intensity)
            b = int(base_color[2] * intensity)
            draw.point((x, y), fill=(r, g, b))

    # Add craters and rugged terrain
    for _ in range(100):  # Number of craters
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        radius = random.randint(10, size // 10)
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                distance = (dx**2 + dy**2)**0.5
                if distance < radius:
                    depth = int((1 - distance / radius) * 50)  # Darken the crater center
                    r, g, b = image.getpixel((x, y))
                    r = max(0, r - depth)
                    g = max(0, g - depth)
                    b = max(0, b - depth)
                    if 0 <= x + dx < size and 0 <= y + dy < size:
                        draw.point((x + dx, y + dy), fill=(r, g, b))

    # Add atmospheric clouds
    cloud_layer = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    cloud_draw = ImageDraw.Draw(cloud_layer)
    for _ in range(30):  # Number of cloud clusters
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        radius = random.randint(10, size // 5)
        cloud_draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=(255, 255, 255, random.randint(30, 70)),  # Semi-transparent white
        )
    image = Image.alpha_composite(image.convert("RGBA"), cloud_layer)

    # Post-process: Add blur for smoothness
    image = image.filter(ImageFilter.GaussianBlur(radius=2))

    # Save the image as a .jpg
    image = image.convert("RGB")  # Convert back to RGB
    image.save(file_path, "JPEG")

    return file_path

texture_path = generate_realistic_planet_texture(size=1024, save_dir="planet_textures")
print(f"Texture saved at: {texture_path}")