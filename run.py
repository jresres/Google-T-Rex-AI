from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import cv2
import numpy as np
import time

# Coordinates of the region to capture (x, y, width, height)
GAME_WINDOW_COORDS = (175, 280, 650, 175)

# (BGR format)
GREEN = (0, 255, 0)

def setupWebdriver():
    # Set up Chrome options
    options = Options()

    # Create the WebDriver instance
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        options=options
    )

    # Return webdriver
    return driver

def captureScreenshot(driver):
    #print(f"[captureScreenshot] taking screenshot")
    screenshot = driver.get_screenshot_as_png()
    image = cv2.imdecode(np.fromstring(screenshot, np.uint8), 0)

    # Crop the image to the specified coordinates
    #print(f"[captureScreenshot] cropping screenshot")
    x, y, w, h = GAME_WINDOW_COORDS
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

def main():
    GAME_URL = 'https://trex-runner.com/'

    driver = setupWebdriver()

    # Open website
    driver.get(GAME_URL)

    # Wait for website to load
    print("[main] loading webpage...waiting 3 seconds")
    time.sleep(3)

    while True:
        startTime = time.time()

        # Capture screenshot
        image = captureScreenshot(driver)

        # Draw a box on the image
        x, y, w, h = GAME_WINDOW_COORDS
        cv2.rectangle(image, (20, 20), (50, 50), (0, 255, 0), 2)

        # Display screenshot
        cv2.imshow('Game Screenshot', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Calculate sleep time to maintain 100ms interval
        elapsedTime = time.time() - startTime
        print(elapsedTime)
        sleepTime = max(0, 0.1 - elapsedTime)
        time.sleep(sleepTime)

    cv2.destroyAllWindows()

    # Close the WebDriver session
    driver.quit()

if __name__ == "__main__":
    main()
