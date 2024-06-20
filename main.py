import cv2
import numpy as np
from time import time
from Capture import GameCapture
from Keystroke import SendKeys

GAME_WINDOW = 'T-Rex Game – Google Dino Run - Google Chrome'

def render_loop():
    gamecap = GameCapture(GAME_WINDOW)
    print("[render_loop] initialized capture settings")

    sendkey = SendKeys(gamecap.hwnd)
    print("[render_loop] initialized key sending")

    print("[render_loop] sending start key")
    sendkey.send_spacebar()

    # OpenCV window to display the video
    print("[render_loop] starting game stream")

    while True:
        # Capture starting time
        start_time = time()

        img = gamecap.take_screenshot()

        cv2.imshow("Game Stream", img)

        #elapsed_time = time() - start_time
        #print(f"FPS: {1 / elapsed_time}")

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[render_loop] game streaming stopped")
            cv2.destroyAllWindows()
            break

    # Exiting render stream
    print("[render_loop] exiting game stream")

def main():
    render_loop()

if __name__ == '__main__':
    main()