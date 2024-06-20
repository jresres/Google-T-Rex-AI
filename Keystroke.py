import win32api
import win32con
import time

class SendKeys:
    def __init__(self, hwnd):
        self.SPACEBAR = win32con.VK_SPACE
        self.UP = win32con.VK_UP
        self.DOWN = win32con.VK_UP
        self.hwnd = hwnd

    def send_keystroke(self, action, keycode):
        win32api.SendMessage(self.hwnd, action, keycode, 0)
        
    def send_spacebar(self):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, self.SPACEBAR, 0)
        time.sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, self.SPACEBAR, 0)

    def press_jump(self):
        self.send_keystroke(win32con.WM_KEYDOWN, self.UP)

    def release_jump(self):
        self.send_keystroke(win32con.WM_KEYUP, self.UP)
    
    def press_duck(self):
        self.send_keystroke(win32con.WM_KEYDOWN, self.DOWN)

    def release_duck(self):
        self.send_keystroke(win32con.WM_KEYUP, self.DOWN)
