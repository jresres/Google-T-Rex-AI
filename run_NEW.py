import win32gui
import win32ui
import win32con
import win32api
import time
import cv2
import numpy as np

FRAME_RATE = 10 # FPS

def enum_windows_callback(hwnd, window_titles):
    if win32gui.IsWindowVisible(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        if window_text:
            window_titles.append(window_text)

def get_all_window_titles():
    window_titles = []
    win32gui.EnumWindows(enum_windows_callback, window_titles)
    return window_titles

def get_monitor_resolution():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def take_screenshot(width, height, x ,y):
    hwnd = win32gui.GetDesktopWindow()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (x,y), win32con.SRCCOPY)
    # dataBitMap.SaveBitmapFile(cDC, output_filename)

    bmpstr = dataBitMap.GetBitmapBits(True)

    # Convert the raw data to an OpenCV image
    img = np.frombuffer(bmpstr, dtype=np.uint8)
    img.shape = (height, width, 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img

def game_loop():
    w = 600 
    h = 200
    x = 650
    y = 400

    # OpenCV window to display the video
    print("[game_loop] starting game stream")

    try:
        while True:
            start_time = time.time()

            img = take_screenshot(w, h, x, y)
            cv2.imshow("Game Stream", img)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            elapsed_time = time.time() - start_time
            print(elapsed_time)
            remaining_time = max(0, 0.1 - elapsed_time)
            time.sleep(remaining_time)
    except KeyboardInterrupt:
        print("[game_loop] game streaming stopped")
    finally:
        cv2.destroyAllWindows()

def main():
    w = 600 
    h = 200
    x = 650
    y = 400
    bmpfilenamename = "out.bmp"

    game_loop()

if __name__ == '__main__':
    main()