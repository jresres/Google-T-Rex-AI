import cv2
import numpy as np
from time import time
from Capture import GameCapture

def game_init():
    GAME_WINDOW = 'T-Rex Game – Google Dino Run - Google Chrome'

    gamecap = GameCapture(GAME_WINDOW)
    print("[game_init] initialized capture settings")
    
    return gamecap

def game_loop(gamecap):

    # OpenCV window to display the video
    print("[game_loop] starting game stream")

    while True:
        start_time = time()

        img = gamecap.take_screenshot()

        cv2.imshow("Game Stream", img)

        elapsed_time = time() - start_time
        print(f"FPS: {1 / elapsed_time}")

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[game_loop] game streaming stopped")
            cv2.destroyAllWindows()
            break

    print("[game_loop] exiting game stream")

def main():
    gamecap = game_init()
    game_loop(gamecap)

if __name__ == '__main__':
    main()