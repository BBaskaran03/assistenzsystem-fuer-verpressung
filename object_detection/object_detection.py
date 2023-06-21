import logging
import sys
from math import atan2

#imports for ObjectDetector
import cv2 as cv
import numpy as np

#from robot_web_services.positions import Position


# class GrabTarget:
#     def __init__(self, position: Position, rotation: float):
#         self.position = position
#         self.rotation = rotation

#     def get_grab_position(self) -> Position:
#         # TODO: Calulate robtarget from self.position
#         return Position.from_worldpoint(0, 0, 0)


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
            _, img = cap.read()
        # Saves the image with name image.jpg
        # cv.imwrite("image.jpg", frame, [cv.IMWRITE_JPEG_QUALITY, 100])
        cap.release()
        return img

    def __adjust_image(self, img, target):
        #crop image for target
        
        if target == 'metal':
            # y:y, x:x
            # TODO: Muss noch angepasst werden
            img = img[100:300, 100:300]
        if target == 'rubber':
            img = img[100:300, 100:300]
        # converts any given image to a grayscale image in order to simplify edge recognition
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.convertScaleAbs(img, 1, 1.7)
        _, img = cv.threshold(img, 210,255, cv.THRESH_BINARY)
        #img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 1)
        return img

    
    def __getOrientation(self, img):
        # find contours
        contours, _= cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        merged_contours = []
        # ignore too small and too big contours and Approximate the contour with convex hull
        for contour in contours:
            # TODO: Check contour size
            area = cv.contourArea(contour)
            if area < 100_000 or 150_000 < area:
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
    
    def move_to_target(self, init_x, init_y, x, y):
        move_x = (init_x-x)/8
        move_y = (init_y-y)/8
        return move_x, move_y


    def get(self, target):
        if target not in ["rubber", "metal"]:
            raise ValueError(f"Unkown target: <{target}>")

        image = self.__capture()
        adjusted_image = self.__adjust_image(image, target)
        
        try:
            x, y, angle = self.__getOrientation(adjusted_image)
        except Exception as e:
            raise Exception ("Fehler in Bildverarbeitung - es konnten keine Kanten gefunden werden")
        
        # TODO: init_x und init_y anpassen
        move_x, move_y = self.move_to_target(1,1, x, y)

        return move_x, move_y, angle   


def main() -> int:
    print("Hello, World")
    object_detector = ObjectDetector()

    move_x, move_y, angle = object_detector.get('rubber')
    print("Gummiteil ist an Position" +str(move_x)+","+ str(move_y)+","+ str(angle)+ ">")

    move_x, move_y, angle = object_detector.get('metal')
    print("Metallteil ist an Position <" +str(move_x)+","+ str(move_y)+","+ str(angle) +">")

    return 0


if __name__ == "__main__":
    sys.exit(main())
