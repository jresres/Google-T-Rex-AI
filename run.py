from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import cv2
import numpy as np
import time

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

def main():
    GAME_URL = 'https://trex-runner.com/'

    driver = setupWebdriver()

    # Open website
    driver.get(GAME_URL)

    # Wait for website to load
    time.sleep(5)

    # Close the WebDriver session
    driver.quit()

if __name__ == "__main__":
    main()
