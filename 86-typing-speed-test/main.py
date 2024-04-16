from ui import TypingSpeedTestUI
from TypingSpeedTest import TypingSpeedTest


if __name__ == '__main__':
    ts_test = TypingSpeedTest()
    # Violates SRP a bit, but is an easy way for the UI to access properties
    # like score etc.
    app = TypingSpeedTestUI(ts_test)
    app.mainloop()
