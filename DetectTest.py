import cv2
import numpy as np

def detect_cactuses(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding the image to get a binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and draw bounding boxes around the detected cactuses
    for contour in contours:
        # Get the bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Filter out smaller or irrelevant contours by size (example size, you may need to adjust)
        if 10 < w < 100 and 10 < h < 100:
            # Draw the bounding box on the original image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the output
    cv2.imshow('Detected Cactuses', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
detect_cactuses('1big.png')