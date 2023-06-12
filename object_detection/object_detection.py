import logging
import sys
#imports for ObjectDetector
import cv2 as cv
from math import atan2
import numpy as np

from robot_web_services.positions import Position


class GrabTarget:
    def __init__(self, position: Position, rotation: float):
        self.position = position
        self.rotation = rotation

    def get_grab_position(self) -> Position:
        # TODO: Calulate robtarget from self.position
        return Position.from_worldpoint(0, 0, 0)


class ObjectDetector:
    def __init__(self):
        pass

    def __adjust_image(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.convertScaleAbs(img, 1, 1.5)
        _, img = cv.threshold(img, 200,255, cv.THRESH_BINARY)
        #img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 1)
        return img

    
    def __getOrientation(self, img):
        # find contours
        contours, _= cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        merged_contours = []
        # ignore too small and too big contours and Approximate the contour with convex hull
        for contour in contours:
            area = cv.contourArea(contour)
            if area < 10000 or 50000 < area:
                continue
            hull = cv.convexHull(contour)
            merged_contours.append(hull)

        # compute center and angle
        merged_contours = sorted(merged_contours, key = cv.contourArea, reverse=True)
        pts = merged_contours[0]
        sz = len(pts)
        data_pts = np.empty((sz, 2), dtype=np.float64)
        for i in range(data_pts.shape[0]):
            data_pts[i,0] = pts[i,0,0]
            data_pts[i,1] = pts[i,0,1]
 
        # Perform PCA analysis
        mean = np.empty((0))
        mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 
        # Center
        x = int(mean[0,0])
        y = int(mean[0,1])

        # orientation in radians
        angle = atan2(eigenvectors[0,1], eigenvectors[0,0])

        # angle in degree
        deg_angle = -int(np.rad2deg(angle)) - 90
        
        return x, y, deg_angle


    def get_position_and_rotation(self, image) -> dict:
        # Example values for location of object
        # At the moment returns x,y pixel-koordinates and rotation in degree
        
        image = cv.imread(image)
        adjusted_image = self.__adjust_image(image)
        try:
            x, y, angle = self.__getOrientation(adjusted_image)
        except Exception as e:
            print("Keine Orientierung gefunden, bitte Objekt neu Poisitionieren")
            print("Error:", e)

        return {"x": x, "y": y, "rotation": angle}

    def get(self, target) -> Position:
        if target not in ["rubber", "metal"]:
            raise ValueError(f"Unkown target: <{target}>")

        position_and_rotation = self.get_position_and_rotation()

        position = Position.from_worldpoint(
            x=position_and_rotation["x"], y=position_and_rotation["y"], z=0
        )
        rotation = position_and_rotation["rotation"]

        grab_target = GrabTarget(position, rotation)
        logging.debug(f"Grab target for <{target}> is: <{grab_target}>")

        grab_position = grab_target.get_grab_position()
        logging.debug(f"Grab position for <{target}> is: <{grab_position}>")

        return grab_position


def main() -> int:
    print("Hello, World")
    object_detector = ObjectDetector()
    object_detector.get_position_and_rotation("rohr (1).jpg")

    position_rubber = object_detector.get("rubber")
    print(f"Gummiteil ist an Position <{position_rubber}>")

    position_metal = object_detector.get("metal")
    print(f"Metallteil ist an Position <{position_metal}>")

    return 0


if __name__ == "__main__":
    sys.exit(main())
