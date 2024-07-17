import pyautogui
import pygetwindow as gw
import keyboard
import time
import subprocess
import sys
import argparse


BROWSER_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BROWSER_WINDOW_TITLE = 'Google Chrome'
SWITCH_TIME = 10


def open_browser_with_tabs(url_list: list[str] = URLS) -> None:
    print("Opening browser with tabs:", url_list)
    subprocess.Popen([BROWSER_PATH, '--new-window'
                      ] + url_list)
    time.sleep(5)
    print("Browser opened, entering full screen mode")
    pyautogui.press('f11')  # Enter full screen mode

    # Optional: Open additional tabs
    """for _ in range(2):  # Adjust if you want more tabs
        pyautogui.hotkey('ctrl', 't')  # Open a new tab
        time.sleep(1)  # Wait for the new tab to open
        pyautogui.typewrite(url)  # Type the URL
        pyautogui.press('enter')  # Press Enter to navigate to the URL
        time.sleep(3)  # Wait for the page to load """


def bring_browser_to_foreground(window_title) -> None:
    windows: list[gw.Win32Window] = gw.getWindowsWithTitle(window_title)
    if windows:
        print("Bringing browser to foreground")
        window = windows[0]
        window.activate()
    else:
        print('Window not found, exiting...')
        sys.exit(1)


def switch_tab() -> None:
    print("Switching to next tab")
    pyautogui.hotkey('ctrl', 'tab')


def refresh_current_tab() -> None:
    print("Refreshing current tab")
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)


def toggle_script():
    global running
    running = not running
    if running:
        print("Script running")
    else:
        print("Script paused. Press Ctrl + Shift + Q to resume")


def listen_for_pause():
    keyboard.add_hotkey('ctrl + shift + q', toggle_script)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Automate browser tab refreshing.')
    parser.add_argument('--urls', nargs='+',
                        help='List of URLs to open in the browser')
    args = parser.parse_args()
    open_browser_with_tabs(args.urls)
    running = True
    print("Script running, press Ctrl + Shift + Q to pause")
    listen_for_pause()

    while True:
        if running:
            original_pointer_pos = pyautogui.position()
            bring_browser_to_foreground(BROWSER_WINDOW_TITLE)
            switch_tab()
            refresh_current_tab()
            print("Returning to original pointer position")
            pyautogui.moveTo(*original_pointer_pos, duration=0.25)
            pyautogui.click()
            time.sleep(SWITCH_TIME)
        else:
            time.sleep(1)
