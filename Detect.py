import cv2

class ObjectVision:
    def __init__(self):
        self.CONTOUR_RETR_MODE = cv2.RETR_EXTERNAL
        self.CONTOUR_APPROX_METHOD = cv2.CHAIN_APPROX_SIMPLE

        self.DUCK_VERTICAL_THRESHOLD = 90 # Y + H for bird boundary box is ~88
        self.WIDTH_THRESHOLD = 30
    
    def get_img_contours(self, img):
        # Grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Thresholding the image to get a binary image
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(binary, self.CONTOUR_RETR_MODE, self.CONTOUR_APPROX_METHOD)

        return contours
    
    def detect_obstacle(self, img, contours):
        nearest_obstacle = [None, None, None] # X, Y + H, W

        # Filter and draw bounding boxes around the detected cactuses
        for contour in contours:
            # Get the bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)

            # Filter out smaller or irrelevant contours by size
            if 10 < w < 100 and 10 < h < 100:
                # Draw the bounding box on the original image
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Put text above the bounding box
                # cv2.putText(img, 'Cactus', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Check for leftmost obstacle position and update if necessary
                if nearest_obstacle[0] is None or x < nearest_obstacle[0]:
                    nearest_obstacle[0] = x
                    nearest_obstacle[1] = y + h
                    nearest_obstacle[2] = w
        
        # Return important coordinates of boundary box for nearest detected object
        return nearest_obstacle
    
    # Return 0 if nearest obstacle is cactus or bird that can be jumped over
    # Return 1 if nearest obstacle is bird that needs to be ducked under
    # Return -1 if no nearest obstacle was detected 
    def classify_nearest_obstacle(self, obstacle):
        print(f"{obstacle[1]}")
        # Check if cactus
        if (obstacle[0] is not None and obstacle[2] < self.WIDTH_THRESHOLD):
            return 0

        # Check if bird that needs to be ducked under
        elif (obstacle[0] is not None and obstacle[1] < self.DUCK_VERTICAL_THRESHOLD):
            return 1
        
        # Check if bird that can be jumped over
        elif (obstacle[0] is not None):
            return 0

        # Neither
        return -1