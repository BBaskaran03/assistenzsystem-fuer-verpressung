import cv2 as cv
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
#cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
#cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
#cam.set(cv.CAP_PROP_EXPOSURE, 8)
#cam.set(cv.CAP_PROP_BACKLIGHT, 8)
  
# reading the input using the camera
result, image = cam.read()
  

if result:
    
    # saving image in local storage
    cv.imwrite("image.jpg", image)
  
# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")
