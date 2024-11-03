import cv2
import numpy as np

file_name = "ex3.jpg"
read_path = r"C:\Users\Pannawit\Documents\GitHub\IoT__CU\Assignment2\Coins\\" + file_name
img = cv2.imread(read_path)

Blur = cv2.medianBlur(img, 3)

dimensions = img.shape
print(dimensions)

grayimg = cv2.cvtColor(Blur, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(grayimg, cv2.HOUGH_GRADIENT, 1.2, dimensions[0] / 50)
thickness = 2
coins = 0

if circles is not None:
    print("Found circle")

    circles = np.uint16(circles[0, :])
    coins = len(circles)
    print(circles)
    print(coins)

    for (x, y, diameter) in circles :
        cv2.circle(img,(x,y), diameter,(0,0,255), thickness,cv2.LINE_AA)
        cv2.circle(img,(x,y), 2,(0,255,0), thickness)
else:
    print("Cannot detect circle.")

text = "Found " + str(coins) + " coins."
position = (dimensions[0] - 100, dimensions[1] - 350)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 255, 0)
thickness = 2

cv2.putText(img, text, position, font, font_scale, color, thickness)

cv2.imshow('Detected circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()