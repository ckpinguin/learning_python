import time
import pyautogui
from PIL import ImageGrab, ImageOps
import numpy as np


# Solution copied from Prasad Khuntias code, with minor modifications

# Region where the dino jumps (left, top, right, bottom)
dino_coords = (696, 420, 3800, 500)
# Region where obstacles appear (left, top, right, bottom)
obstacle_coords = (881, 420, 3600, 500)


def check_obstacle():
    image = ImageGrab.grab(bbox=obstacle_coords)
    gray_image = ImageOps.grayscale(image)
    a = np.array(gray_image.getcolors())
    return a.sum() < 1000


def jump():
    pyautogui.keyDown('space')
    time.sleep(0.05)
    pyautogui.keyUp('space')


print("Starting game in 3 seconds...")
time.sleep(3)

while True:
    if check_obstacle():
        jump()
        time.sleep(0.1)
    time.sleep(0.1)
