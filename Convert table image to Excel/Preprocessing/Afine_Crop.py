import cv2
import numpy as np
import matplotlib.pyplot as plt
input_image2 = cv2.imread('New folder/test7.jpg')


orig_img_coor = np.float32([[9,145],[2461,165],[9,1769],[2457,1777]])

height , width = input_image2.shape[0] ,input_image2.shape[1]

new_img_coor = np.float32([[0,0],[width,0],[0,height],[width,height]])

p = cv2.getPerspectiveTransform(orig_img_coor, new_img_coor)
perspective = cv2.warpPerspective(input_image2, p ,(width,height))
cv2.imwrite('rotatedtyt_image.jpg', perspective)