# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:15:27 2019
@author: batho
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import harris2
import matplotlib.pyplot as plt
import detect_up

def filter_color(rgb_image, lower_bound_color, upper_bound_color):
    #convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)
    return mask

def getContours(binary_image):
    
    _, contours, hierarchy = cv2.findContours(binary_image.copy(), 
                                            cv2.RETR_EXTERNAL,
	                                        cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_ball_contour(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    for c in contours:
        area=cv2.contourArea(c)
        #print(area)
        #perimeter= cv2.arcLength(c, True)
        #((x, y), radius) = cv2.minEnclosingCircle(c)
        #print('x,y,radius', x,y,radius)
        #Note for competetion the range has to be decided carefully
        if (area >5000):
            #print('area: ', area)
            #cv2.drawContours(rgb_image, [c], -1, (0,250,255), 1)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            #cv2.drawContours(black_image, [c], -1, (0,250,150), 1)
            cx, cy = get_contour_center(c)
            #cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            #cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            #cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)
            #count+=1
            #print ("Area: {}, Perimeter: {}".format(area, perimeter))
            #print('Sign detected= red')
            return True, x,y,radius
    return False,0,0,0

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    #print(cx,cy)
    return cx, cy

def pipeline(image):
    #Red
    lower =(100, 40, 70)
    upper = (105, 215, 180)
    
    #green
    #lower =(55, 75, 120)
    #yellow
    #lower=(25,80,180)
    #blue
    #lower(105,120,180)
    #ret,frame = cap.read()
    #rgb_image = read_rgb_image(frame, True)
    binary_image_mask = filter_color(image, lower, upper)
    contours = getContours(binary_image_mask)
    check, x,y,radius=draw_ball_contour(binary_image_mask, image,contours)
    return check, int(x),int(y),int(radius)


'''
my=cv2.imread('Up.jpg')
track=0
checking=True
_,x,y,radius=pipeline(my)
roi2=my[int(y-(radius)):int((y+radius)),x-(radius):int((x+radius))]
#cv2.imwrite('up_roi.jpg', roi2)
roi3=roi2[int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36),:]
roi4=roi2[:,int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36)]
#cv2.imwrite('up_roi2.jpg', roi3)
plt.imshow(roi4)
result, count=harris2.find_corners(roi3)
result_up, count_up=detect_up.find_up(roi4)
if count_up>count:
    result='up'
else:
    result=result
print(result)
'''
'''
if result=='U':
    while checking:
        track+=1
        if track==1:
            roi3=roi2[:,int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36)]
            result=detect_up.find_up(roi3)
            print(result)
            if result=='up':
                break
            else:
                print('could not detect anything proceeding with caution')
                track=0
                break
'''
'''
#Video Demo
check=[]
for i in range(85):
    my=cv2.imread('video_seperate/Frame_{}.jpg'.format(i))
    #plt.imshow(my)
    #my=my[int(my.shape[1]/3.8):int(my.shape[1]/1.36),:]
    #print(my)
    _,x,y,radius=pipeline(my)
    #cv2.imshow('my', my)
    #cv2.waitKey()
    roi2=my[int(y-(radius)):int((y+radius)),x-(radius):int((x+radius))]
    #plt.imshow(roi2)
    #print(roi2.shape)
    roi3=roi2[int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36),:]
    roi4=roi2[:,int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36)]
    pred, count =harris2.find_corners(roi3)
    pred_up, count_up =detect_up.find_up(roi4)
    if count_up>count:
        pred='up'
    check.append(pred)
    print(i)
    
count=0
for j in check:
    if j=='left':
        count+=1
print((count/84)*100)
'''



#Image capture

cam =cv2.VideoCapture(0)
cv2.namedWindow('result')

while True:
    ret, frame=cam.read()
    frame=cv2.rotate(frame,cv2.ROTATE_180)
    #frame=frame[int(frame.shape[1]/3.8):int(frame.shape[1]/1.36),:]
    check,x,y,radius=pipeline(frame)
    #print(x,y,radius)
    if check:
        track=0
        checking=True
        roi2=frame[y-radius:y+radius, x-radius:x+radius]
        roi3=roi2[int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36),:]
        roi4=roi2[:,int(roi2.shape[1]/3.8):int(roi2.shape[1]/1.36)]
        pred, count =harris2.find_corners(roi3)
        pred_up, count_up =detect_up.find_up(roi4)
        if count_up>count:
            pred='up'
            
        
        frame=cv2.putText(frame,pred,(50,50),cv2.FONT_HERSHEY_SIMPLEX,
                          1,(255,0,0), 2,cv2.LINE_AA)
        
        #cv2.imshow(roi)
    else:
        pass
    cv2.imshow('out', frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    #cv2.imshow('roi', roi)
    #cv2.imwrite('roi_left.jpg', roi)
    #plt.imshow(my)
    #cv2.imshow('result',my)
#cv2.imshow('final', out_img)
cam.release()
cv2.destroyAllWindows() 