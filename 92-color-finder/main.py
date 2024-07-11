from PIL import Image
import argparse
import numpy as np
from collections import Counter

# Define main color categories with representative RGB values
color_categories = {
    'white-ish': (255, 255, 255),
    'black-ish': (0, 0, 0),
    'red-ish': (255, 0, 0),
    'green-ish': (0, 255, 0),
    'blue-ish': (0, 0, 255),
    'yellow-ish': (255, 255, 0),
    'cyan-ish': (0, 255, 255),
    'magenta-ish': (255, 0, 255),
    'grey-ish': (128, 128, 128),
    # Add more categories as needed
}


def rgb_to_hex(rgb: int):
    """Convert an RGB tuple to a hex string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def euclidean_distance(color1, color2):
    """Calculate the Euclidean distance between two RGB colors."""
    return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))


def categorize_color(color):
    """Categorize a color by finding the nearest category
    based on Euclidean distance."""
    distances = {category: euclidean_distance(
        color, rep_color) for category, rep_color in color_categories.items()}
    return min(distances, key=distances.get)


def analyze_image_colors(img_path: str, num_colors: int = 5) -> None:
    img = Image.open(img_path)
    img = img.convert('RGB')

    img_array = np.array(img)

    pixels = img_array.reshape(-1, 3)

    # Categorize each pixel color
    categorized_colors = [categorize_color(tuple(pixel)) for pixel in pixels]

    # Count occurrences of each color
    color_counts = Counter(categorized_colors)

    # Get the most common colors
    main_colors = color_counts.most_common(
        num_colors)  # Adjust the number as needed

    return main_colors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find main colors in an image.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')

    args = parser.parse_args()

    main_colors = analyze_image_colors(args.image_path, 20)
    print(main_colors)
    # main_colors_hex = [(rgb_to_hex(color), count)
    # for color, count in main_colors]
    # print(main_colors_hex)
