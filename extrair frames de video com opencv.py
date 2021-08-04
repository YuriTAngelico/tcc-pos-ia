import cv2
print(cv2.__version__)

import os
print(os.path.dirname(os.path.realpath(__file__)) + '\\buny.mp4')

source  = cv2.VideoCapture(os.path.dirname(os.path.realpath(__file__)) + '\\buny.mp4')
# cap = cv2.VideoCapture(0)

success,image = source.read()
count = 0
while count < 5:
  cv2.imwrite(os.path.dirname(os.path.realpath(__file__)) + f"\\frame{count}.jpg", image)     # save frame as JPEG file      
  success,image = source.read()
  print('Read a new frame: ', success)
  count += 1