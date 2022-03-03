from spots_detection import empty_spots_detection as d_spots
import numpy as np
import cv2


def get_available_spots(image,id):
    alpha = 0.5
    empty_spots=d_spots.detect_empty_spots(image,id)
    cp_image = np.copy(image)
    new_image = np.copy(image)
    amount=len(empty_spots[0])+len(empty_spots[1])+len(empty_spots[2])
    for i in range(len(empty_spots)):
        for box in empty_spots[i]:
            x1, y1, x2, y2 = box
            cv2.rectangle(cp_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), -1)
    cv2.addWeighted(cp_image, alpha, new_image, 1 - alpha, 0, new_image)
    cv2.putText(new_image, "Total: %d" % amount, (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    return new_image