# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:35:34 2019
@author: batho
"""

import cv2 
import numpy as np 
import matplotlib.pyplot as plt
  
# path to input image specified and  
# image is loaded with imread command 
#image = cv2.imread('roi_left.jpg')
#plt.imshow(image)
def find_corners(roi):  
    # convert the input image into 
    # grayscale color space
    try:
        operatedImage = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) 
      
    # modify the data type 
    # setting to 32-bit floating point 
        operatedImage = np.float32(operatedImage)
  
        # apply the cv2.cornerHarris method 
        # to detect the corners with appropriate 
        # values as input parameters 
        dest = cv2.cornerHarris(operatedImage, 4, 17, 0.05) 
          
        # Results are marked through the dilated corners 
        dest = cv2.dilate(dest, None) 
          
        # Reverting back to the original image, 
        # with optimal threshold value 
        roi[dest > 0.12 * dest.max()]=[0, 0, 255]
        
        ret, dest = cv2.threshold(dest,0.12*dest.max(),255,0)
        dest = np.uint8(dest)
        
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dest)
        
        left_count=0
        right_count=0
        count_up=0
        #up_count=0
        half=int(roi.shape[1]/2)
        for c in centroids:
            #if c[1]<half_up:
                #count_up+=1
            if c[0]<half:
                left_count+=1
            else:
                right_count+=1
        if count_up>4:
            print(count_up)
            print('going up')
            return 'up'
        if left_count>right_count:
            print('Yo mama turn left')
            print('left:', left_count)
            return 'left', left_count
        else:
            print('Stupid thats right')
            print('right:', right_count)
            return 'right', right_count
    except:
        print('Could not read image exceeds threshold')
        return 'nothing', 0
  
# the window showing output image with corners 
#cv2.imshow('Image with Borders', image) 
  
# De-allocate any associated memory usage  
#if cv2.waitKey(0) & 0xff == 27: 
#    cv2.destroyAllWindows() 