#!/usr/bin/env python3
import cv2 as cv                                                                #Importing opencv module
import math                                                                     #Importing math module
import numpy as np                                                              #Importing numpy module
import rospy
from turtlesim.msg import Pose

rospy.init_node("bot_pose")
pub=rospy.Publisher("/bot/pose", Pose, queue_size = 5)
locate=Pose()

def mousePoints(event, x, y, flags, params):                                     #Function to display points or coordinates marked on screen or arena
    if event == cv.EVENT_LBUTTONDOWN:
        ListOfPoints.append([x, y])
        print(ListOfPoints)
                
cap = cv.VideoCapture(1)                                                         #Capturing frames
_, frame1 = cap.read()                                                           #Reading the frames
_, frame2 = cap.read()

ListOfPoints = []                                                                #List to save the points or coordinates

cv.namedWindow('frame1')  
cv.setMouseCallback('frame1', mousePoints)                                       #On user click the function to display the coordinates will be called

while True:

    img = cv.absdiff(frame1, frame2)                                            #Difference of two read images
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)                               #Converting the image to Gray
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 0)                               #Blurring the Gray image
    
    _, thresh = cv.threshold(imgBlur, 20, 255, cv.THRESH_BINARY)                #Creating the threshold image of blurred image
    imgDilation = cv.dilate(thresh, None, iterations = 3)                       #Dilating the threshold image

    contours, hierarchy = cv.findContours(imgDilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) #Finding contours of dilated image

    for cnt in contours:
        area = cv.contourArea(cnt)
        
        if area>500:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.1 * peri, True)
            
            x, y, w, h = cv.boundingRect(cnt)                                  #Points to create rectangle

            cv.rectangle(frame1, (x, y), (x + w, y + h), (255, 255, 0), 5)     #Displaying Rectangle on frame
            Cx = int(x + (w/2))                                                # X coordinate of center of rectangle 
            Cy = int(y + (h/2))                                                # Y coordinate of center of rectangle 
            locate.x = Cx
            locate.y = Cy

            pub.publish(locate)
            cv.circle(frame1, (Cx, Cy), 7, (255, 0, 0), -1)
    
    cv.imshow("frame1", frame1)                                               #Showing frame

    frame1 = frame2
    _, frame2 = cap.read()

    if cv.waitKey(1) & 0XFF == ord('q'):                                      #Closing all windows
        break

cap.release()
cv.destoryAllWindows()