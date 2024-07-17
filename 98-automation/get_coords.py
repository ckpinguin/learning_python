import pyautogui
import time

while True:
    x, y = pyautogui.position()
    print(f"Position: ({x}, {y})")
    time.sleep(1)
