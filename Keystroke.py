import win32api
import win32con
import time

class SendKeys:
    def __init__(self, hwnd):
        self.SPACEBAR = win32con.VK_SPACE
        self.UP = win32con.VK_UP
        self.DOWN = win32con.VK_UP
        self.hwnd = hwnd

    def send_keystroke(self, keycode):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, keycode, 0)
        time.sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, keycode, 0)
        
    def send_spacebar(self):
        self.send_keystroke(self.SPACEBAR)

    def send_jump(self):
        self.send_keystroke(self.UP)
    
    def send_duck(self):
        self.send_keystroke(self.DOWN)