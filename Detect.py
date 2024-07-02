import cv2

class ObjectVision:
    def __init__(self):
        self.CONTOUR_RETR_MODE = cv2.RETR_EXTERNAL
        self.CONTOUR_APPROX_METHOD = cv2.CHAIN_APPROX_SIMPLE

        self.DUCK_VERTICAL_THRESHOLD = 90 # Y + H for bird boundary box is ~88
        self.WIDTH_THRESHOLD = 30
        self.CLUSTER_EDGE_THRESHOLD = 5
    
    def get_img_contours(self, img):
        # Grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Thresholding the image to get a binary image
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(binary, self.CONTOUR_RETR_MODE, self.CONTOUR_APPROX_METHOD)

        return contours
    
    def detect_obstacles(self, img, contours):
        obstacles = [] # X, Y + H, W

        # Filter and draw bounding boxes around the detected cactuses
        for contour in contours:
            # Get the bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)

            # Filter out smaller or irrelevant contours by size
            # Filter out dinosaur when ducking
            if 10 < w < 100 and 10 < h < 100 and x > 5:
                # Draw the bounding box on the original image
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Put text above the bounding box
                # cv2.putText(img, 'Cactus', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                obstacles.append([x, y + h, w])
        
        # Return important coordinates of boundary box for nearest detected object
        return obstacles
    
    # Sort obstacle coordinates in increasing x coordinate value order
    def sort_obstacles(self, obstacles):
        return sorted(obstacles, key=lambda x: x[0])

    # returns array of boundary box coordinates of closest object [X, Y+H, W]
    def get_nearest_obstacle(self, obstacles):
        if obstacles:
            return obstacles[0]
        else:
            return None

    # Input should be sorted obstacles
    def get_cluster_length(self, obstacles):
        num_cactus = 1
        for i in range(len(obstacles) - 1):
            box_redge = obstacles[i][0] + obstacles[i][2]
            next_box_ledge = obstacles[i + 1][0]
            if (next_box_ledge < (box_redge + self.CLUSTER_EDGE_THRESHOLD)):
                num_cactus = num_cactus + 1
            else:
                break
                    
        if obstacles:
            cluster_length = (obstacles[num_cactus - 1][0] + obstacles[num_cactus - 1][2]) - obstacles[0][0]    

            # print(cluster_length)

    # Return 0 is duck needed, otherwise return 1 for a jump
    def determine_action(self, obstacle):
        # Check if bird that needs to be ducked under
        if (obstacle[1] < self.DUCK_VERTICAL_THRESHOLD):
            return 0
        
        # Obstacle can be jumped over
        else:
            return 1