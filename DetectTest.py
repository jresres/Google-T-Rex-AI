import cv2
import numpy as np

CLUSTER_EDGE_THRESHOLD = 5

def get_num_cactus(boxes):
    num_cactus = 1

    # print(boxes)

    for i in range(len(boxes) - 1):
        box_redge = boxes[i][0] + boxes[i][1]
        next_box_ledge = boxes[i + 1][0]
        if (next_box_ledge < (box_redge + CLUSTER_EDGE_THRESHOLD)):
            num_cactus = num_cactus + 1
        else:
            break

    print(f"Number of cactus in nearest cluster: {num_cactus}")

    cluster_length = (boxes[num_cactus - 1][0] + boxes[num_cactus - 1][1]) - boxes[0][0]         

    print(f"Length of cactus cluster: {cluster_length}")

def detect_object(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding the image to get a binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    nearest_obstacle = [None, None] # X, Y + H

    box_coords = []

    # Filter and draw bounding boxes around the detected object
    for contour in contours:
        # Get the bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Filter out smaller or irrelevant contours by size
        if 10 < w < 35 and 10 < h < 100:
            # Draw the bounding box on the original image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            box_coords.append([x,w])

            if (w >= 30):
                # Put text above the bounding box
                cv2.putText(image, 'Bird', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                # Put text above the bounding box
                cv2.putText(image, 'Cactus', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if nearest_obstacle[0] is None or x < nearest_obstacle[0]:
                    nearest_obstacle[0] = x
                    nearest_obstacle[1] = y + h

    box_coords = sorted(box_coords, key=lambda x: x[0])

    get_num_cactus(box_coords)

    # Display the output
    cv2.imshow('Detected Cactuses', image)
    cv2.waitKey(0)

# Example usage
# detect_object('bird.png')
detect_object('1big.png')
# detect_object('1big.png')
detect_object('1small.png')
detect_object('3small.png')
cv2.destroyAllWindows()
