import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt

#SHAPE DETECTION ZA IZDVAJANJE LOPTICE - GLEDAJ DA L VRACA CENTRALNU KOORDINATU LOPTICE ILI NEKU IVICU
#SKONTAJ KAKO DA IZDVOJIS ZIDOVE

# img = cv2.imread('slika.png',5)
# edges = cv2.Canny(img,100,200)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# Create a VideoCapture object and read from input file

# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('video1.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed

counter = 0
while(cap.isOpened()):
  counter += 1
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Display the resulting frame
    cv2.imshow('Frame',frame)
    edges = cv2.Canny(frame,300,400)
    plt.subplot(121),plt.imshow(frame,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    if counter % 50 == 0:
        plt.show()

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):

      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()