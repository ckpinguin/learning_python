import pyautogui
import pygetwindow as gw
import time
import subprocess
import sys


BROWSER_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URLS = ['https://www.google.com',
        'https://udemy.com', 'https://www.youtube.com']


TAB_POSITIONS = [
    (250, 50),
    (600, 50),
    (1000, 50)
]


def open_browser_with_tabs(url_list: list[str] = URLS):
    subprocess.Popen([BROWSER_PATH, '--new-window',
                     '--start-fullscreen'] + url_list)
    time.sleep(10)

    # Optional: Open additional tabs
    """for _ in range(2):  # Adjust if you want more tabs
        pyautogui.hotkey('ctrl', 't')  # Open a new tab
        time.sleep(1)  # Wait for the new tab to open
        pyautogui.typewrite(url)  # Type the URL
        pyautogui.press('enter')  # Press Enter to navigate to the URL
        time.sleep(3)  # Wait for the page to load """


def refresh_tab(position: tuple[int]):
    pyautogui.click(position)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'r')


def bring_browser_to_foreground(window_title):
    windows: list[gw.Win32Window] = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.activate()
        window.maximize()
    else:
        print('Window not found, exiting...')
        sys.exit(1)


if __name__ == '__main__':
    open_browser_with_tabs(URLS)
    browser_window_title = "Google Chrome"

    while True:
        bring_browser_to_foreground(browser_window_title)
        for position in TAB_POSITIONS:
            refresh_tab(position)
            time.sleep(60 / len(TAB_POSITIONS))
