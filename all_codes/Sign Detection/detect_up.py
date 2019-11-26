# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:13:38 2019
@author: batho
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

def find_up(image):
    try:
        operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        half=int(image.shape[0]/2)  
        # modify the data type 
        # setting to 32-bit floating point 
        operatedImage = np.float32(operatedImage)
          
        # apply the cv2.cornerHarris method 
        # to detect the corners with appropriate 
        # values as input parameters 
        dest = cv2.cornerHarris(operatedImage, 4, 19, 0.06) 
        image[dest > 0.12 * dest.max()]=[0, 0, 255]
          
        # Results are marked through the dilated corners 
        ret, dest = cv2.threshold(dest,0.12*dest.max(),255,0)
        dest = np.uint8(dest)
        
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dest)
        up=0
        nothing=0
        for c in centroids:
            if c[1]<half:
                up+=1
                
            else:
                nothing+=1
                
        if up>nothing:
            print('Going Up')
            return 'up', up
        else: return 'nothing',0
    except:
        print('Exceeds Thresshold')
        return 'nothing',0        
# Reverting back to the original image, 
# with optimal threshold value 

#cv2.imshow('res', image)
#cv2.waitKey()