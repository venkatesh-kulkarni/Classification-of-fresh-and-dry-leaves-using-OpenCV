# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# importing the necessary libraries
import numpy as np
import cv2

# reading the image from local directory
img = cv2.imread('C:/Users/Venkatesh/Downloads/leaves2.jpg', 1)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# converting the colored image to gray scale image
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# specifying the threshold values for the contour
ret, thresh = cv2.threshold(imgray, 230, 255, cv2.THRESH_BINARY)     # by trial and error method, I found the value of the second argument (230) to be the most accurate

# storing the contours (I took only two arguments in the LHS as taking 3 arguments was throwing an error)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:                               # iterating over the contours

    area = cv2.contourArea(cnt)                            # calculating the area of each detected contour

    peri = cv2.arcLength(cnt, True)                        # calculating the perimeter of each contour
    approx = cv2.approxPolyDP(cnt, 0.02*peri, True)        # approximating the contour as a polygon; this step is essential to make bounding boxes

    x,y,w,h = cv2.boundingRect(approx)                     # defining the bounding boxes

    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,0), 2)    # creating bounding boxes of thickness 2.

    color = np.array(cv2.mean(hsv[y:y + h, x:x + w])).astype(np.uint8)       # taking the mean of pixels of contour from the hsv form of the image to apply the condition of dry
                                                                             # and fresh leaves on the average value of those pixels

    print(color)                                                             # checking out the values obtained. Here we obtain a (4,1) matrix for each contour with the
                                                                             # first three values of each row representing the HSV values respectively.
    if(color[0]>39 and color[0]<90):                                         # the hue value of green is 60 and that of yellow is 30. Applying the equation G/(G+Y)>0.7, we get a value of 39.
            objectType = "fresh"

    else:
        objectType = "old"

    cv2.putText(img, objectType, (x+w//4, y+h+10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,0,0),1)           # writing the text output on the image


img = cv2.drawContours(img, contours, -1, (0,233,233), 2)

cv2.imshow('img', img)

cv2.waitKey(0)

cv2.destroyAllWindows()


