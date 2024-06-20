import cv2
from time import time
from Capture import GameCapture
from Keystroke import SendKeys
from Detect import ObjectVision

GAME_WINDOW = 'T-Rex Game – Google Dino Run - Google Chrome'

JUMP_DISTANCE_THRESHOLD = 100

# scale jumping threshold with time

def render_loop():
    gamecap = GameCapture(GAME_WINDOW)
    print("[render_loop] initialized capture settings")

    sendkey = SendKeys(gamecap.hwnd)
    print("[render_loop] initialized key sending")

    vision = ObjectVision()
    print("[render_loop] initialized object vision")

    sendkey.send_spacebar()
    print("[render_loop] sent start key")

    # OpenCV window to display the video
    print("[render_loop] starting game stream")

    while True:
        # Capture starting time
        start_time = time()

        # Take screenshot
        img = gamecap.take_screenshot()

        # Get image contours
        contours = vision.get_img_contours(img)

        # Copy image to make writeable  
        rendered_img =  img.copy()

        # Returns closest obstacle boundary box coordinates
        nearest_obstacle = vision.detect_obstacle(rendered_img, contours)

        # Check if object is within jumping/ducking distance
        if (nearest_obstacle[0] is not None and nearest_obstacle[0] < JUMP_DISTANCE_THRESHOLD):

            # Get what type of object is in front of dinosaur
            classified_nearest_obstacle = vision.classify_nearest_obstacle(nearest_obstacle)

            # Jump over cactus/bird
            if (classified_nearest_obstacle == 0):
                sendkey.press_jump()

            # Duck under bird
            elif (classified_nearest_obstacle == 1):
                sendkey.press_duck()

        # Show rendered image
        cv2.imshow("Game Stream", rendered_img)

        # elapsed_time = time() - start_time
        # print(f"FPS: {1 / elapsed_time}")

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