import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find main colors in an image.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')

    args = parser.parse_args()
