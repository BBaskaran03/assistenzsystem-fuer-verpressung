import logging
import sys
from math import atan2

#imports for ObjectDetector
import cv2 as cv
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

    def __capture(self):
        # captures an imagage with the camera on channel 0
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)

        # focus set to 20 due to problems with autofocus may adjust this
        focus = 20
        cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)
        cap.set(cv.CAP_PROP_FOCUS, focus)

        for index in range(20):
            ret, frame = cap.read()
        # Saves the image with name image.jpg
        cv.imwrite("image.jpg", frame, [cv.IMWRITE_JPEG_QUALITY, 100])
        cap.release()

    def __adjust_image(self, img):
        # converts any given image to a grayscale image in order to simplify edge recognition
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.convertScaleAbs(img, 1, 1.5)
        _, img = cv.threshold(img, 200,255, cv.THRESH_BINARY)
        #img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 1)
        return 0

    
    def __getOrientation(self, img):
        # find contours
        contours, _= cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        merged_contours = []
        # ignore too small and too big contours and Approximate the contour with convex hull
        for contour in contours:
            # TODO: Check contour size
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
        # At the moment returns x,y pixel-koordinates and rotation in degree
        self.__capture()
        image = cv.imread("image.jpg")
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
