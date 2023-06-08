import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
import numpy as np
 
def adjust_brightness_contrast(image, brightness, contrast):
    adjusted_image = cv.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted_image

def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
 
  ## [visualization1]
  angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
  ## [visualization1]
 
def getOrientation(pts, img):
  ## [pca]
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
 
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 
  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
  ## [pca]
 
  ## [visualization]
  # Draw the principal components
  cv.circle(img, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  drawAxis(img, cntr, p1, (255, 255, 0), 0.25)
  drawAxis(img, cntr, p2, (0, 0, 255), 2)
 
  angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
  ## [visualization]
 
  # Label with the rotation angle
  label = "  Rotation Angle: " + str(-int(np.rad2deg(angle)) - 90) + " degrees"
  textbox = cv.rectangle(img, (cntr[0], cntr[1]-25), (cntr[0] + 250, cntr[1] + 10), (255,255,255), -1)
  cv.putText(img, label, (cntr[0], cntr[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
 
  return angle, cntr
 
def main(image):
    print(image)
    # Load the image
    img = cv.imread(image)

    # Was the image there?
    if img is None:
        print("Error: File not found")
        exit(0)

    # Convert image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = adjust_brightness_contrast(gray, -500, 5)


    blurred = cv.blur(gray, (10, 10), 0)
    thresh = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 19, 1)


    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(thresh)

    cv.imwrite("gray.jpg", gray)

    # Convert image to binary
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)

    # Find all the contours in the thresholded image
    contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    merged_contours = []
    for contour in contours:
        # Calculate the area of each contour
        area = cv.contourArea(contour)

        # Ignore contours that are too small or too large
        if area < 50000 or 150000 < area:
            continue

        # Approximate the contour with convex hull
        hull = cv.convexHull(contour)

        # Add the approximated contour to the merged contours list
        merged_contours.append(hull)

    # Draw largest of merged contours

    merged_contours = sorted(merged_contours, key=cv.contourArea, reverse=True)

    try:
        largest_contour = merged_contours[0]
        cv.drawContours(img, [largest_contour], -1, (0, 0, 255), 2)

        #print(-int(np.rad2deg(getOrientation(largest_contour, img))) - 90)

        angle, center  = getOrientation(largest_contour, img)
        print("Rotation Angle:", -int(np.rad2deg(angle)) - 90)
        print("Center:", center)
        # Save the output image to the current directory
        cv.imwrite("out_"+image, img)

    except:
       print("Error please reposition the coponent") 

for i in range(1,44):
   
   main("Rohr ("+ str(i)+").jpg")


"""
Variablen zum rumspielen:
Z.103 (area<50000)






"""