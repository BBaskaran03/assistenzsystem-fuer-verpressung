import cv2 as cv

cam = cv.VideoCapture(0)

result, image = cam.read()

cv.imshow("HI", image)
cv.imwrite("image.png", image)

cv.waitKey(0)
cv.destroyWindow("HI")