import numpy as np
import win32gui, win32ui, win32con

class GameCapture:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.screen_width = window_rect[2] - window_rect[0]
        self.screen_height = window_rect[3] - window_rect[1]

        # define dino game window
        self.game_width = 600
        self.game_height = 150

        # adjust crop settings
        border_pixels = 8
        desc_pixels = (2 * 30) + 185 # 30 pixel padding below and above description text
        button_pixels = (2 * 10) + 23 # 10 pixel padding above and below button div
        header_pixels = 125 + desc_pixels + button_pixels
        self.screen_width = self.screen_width - (border_pixels * 2)
        self.screen_height = self.screen_height - header_pixels
        self.cropped_x = border_pixels + int((self.screen_width - self.game_width) / 2)
        self.cropped_y = header_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def take_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.game_width, self.game_height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.game_width, self.game_height) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        bmpstr = dataBitMap.GetBitmapBits(True)

        # Convert the raw data to a format opencv can read
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (self.game_height, self.game_width, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)