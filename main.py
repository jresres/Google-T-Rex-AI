import cv2
from time import time, sleep
from Capture import GameCapture
from Keystroke import SendKeys
from Detect import ObjectVision

# TODO: never stops ducking after seeing bird
# TODO: get cluster of cactus length

FPS = 120
GAME_WINDOW = 'T-Rex Game – Google Dino Run - Google Chrome'

JUMP_DISTANCE_THRESHOLD = 100

ACTION_DBG_MODE = False

# scale jumping threshold with time

def render_loop():
    gamecap = GameCapture(GAME_WINDOW)
    print("[render_loop] initialized capture settings")

    sendkey = SendKeys(gamecap.hwnd, ACTION_DBG_MODE)
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

        group = []

        # Take screenshot
        img = gamecap.take_screenshot()

        # Get image contours
        contours = vision.get_img_contours(img)

        # Copy image to make writeable  
        rendered_img =  img.copy()

        # Returns array of all obstacle coordinates detected sorted
        obstacles = vision.sort_obstacles(vision.detect_obstacles(rendered_img, contours))

        vision.get_cluster_length(obstacles)

        # Returns closest obstacle boundary box coordinates
        nearest_obstacle = vision.get_nearest_obstacle(obstacles)

        # Check if object is within jumping/ducking distance
        if (nearest_obstacle is not None and nearest_obstacle[0] < JUMP_DISTANCE_THRESHOLD):

            # Get what type of object is in front of dinosaur
            action = vision.determine_action(nearest_obstacle)

            # Set duck count to FPS
            if (action == 0):
                sendkey.press_duck()

            elif (action == 1):
                sendkey.press_jump()

        # Show rendered image
        cv2.imshow("Game Stream", rendered_img)

        elapsed_time = time() - start_time
        # print(f"FPS: {1 / elapsed_time}")
        remaining_time = max(0, (1 / FPS) - elapsed_time)
        sleep(remaining_time)

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