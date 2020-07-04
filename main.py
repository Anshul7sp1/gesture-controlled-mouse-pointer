import cv2
import math
import time
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False

def nothing(x):
    pass

def distance(c1, c2):
    c1 = np.array(c1)
    c2 = np.array(c2)
    res = math.sqrt(pow((c1[0]-c2[0]), 2) + pow((c1[1]-c2[1]), 2))
    res = int(res)
    return res

cv2.namedWindow("Hue")
cv2.namedWindow("Saturation")
cv2.namedWindow("Value")

cv2.createTrackbar("L_b", "Hue", 0, 255, nothing)
cv2.createTrackbar("U_b", "Hue", 255, 255, nothing)
cv2.createTrackbar("L_b", "Saturation", 0, 255, nothing)
cv2.createTrackbar("U_b", "Saturation", 255, 255, nothing)
cv2.createTrackbar("L_b", "Value", 0, 255, nothing)
cv2.createTrackbar("U_b", "Value", 255, 255, nothing)

front_camera = 0
cap = cv2.VideoCapture(front_camera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
screen_width, screen_height = pyautogui.size()
print("Screen Dimensions", screen_width, ":", screen_height)
print("Feed Dimensions", width, ":", height)

ratio = 2
scale = np.array([(screen_width/width)*ratio, (screen_height/height)*ratio])

pixel_thresh = 10
prev_pt = (0, 0)
click_thresh = 150
finger_dist = 1000
touched = False
clicked = False 
mouse_down = False
duration = 10
mouse_duration = 0.01
dis = 0

while cap.isOpened():
    ret, image = cap.read()

    image = cv2.flip(image, 1)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hlb = cv2.getTrackbarPos("L_b", "Hue")
    hub = cv2.getTrackbarPos("U_b", "Hue")
    slb = cv2.getTrackbarPos("L_b", "Saturation")
    sub = cv2.getTrackbarPos("U_b", "Saturation")
    vlb = cv2.getTrackbarPos("L_b", "Value")
    vub = cv2.getTrackbarPos("U_b", "Value")

    l_b = np.array([hlb, slb, vlb])
    u_b = np.array([hub, sub, vub])

    mask = cv2.inRange(hsv_image, l_b, u_b)
    mask = cv2.medianBlur(mask, 3)
    contour, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    new_contour = []
    for i, cntr in zip(range(len(contour)), contour) :
        (x, y, w, h) = cv2.boundingRect(cntr)
        if cv2.contourArea(cntr) > 500 and heirarchy[0][i][3] == -1:
            new_contour.append(cntr)
    contour = sorted(new_contour, key=lambda x: cv2.contourArea(x))
    contour = contour[::-1]
    contour = contour[:2]

    pt = []
    for cntr in contour :
        (x, y, w, h) = cv2.boundingRect(cntr)
        pt.append(((int)(x+w/2), (int)(y+h/2)))
        cv2.circle(image, ((int)(x+w/2), (int)(y+h/2)), 2, (0, 255, 255), 3)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    l = len(pt)

    if l == 2:
        clicked = False
        if touched :
            touched = False
            end = time.time()
            duration = end - start
            if duration < 0.3 :#and duration < 1.0:
                pyautogui.click()
                print("clicked", finger_dist)
            else:
                if mouse_down:
                    pyautogui.mouseUp()
                    mouse_down = False
                    print("mouse Up", finger_dist)
                
        finger_dist = distance(pt[0], pt[1])
        # print(finger_dist)
        mid_point = tuple((np.array(pt[0]) + np.array(pt[1]))/2)
        mid_point = np.array(mid_point, int)
        move_point = tuple(((mid_point-np.array((500,170)))*scale)) #- np.array(pyautogui.position()))
        dis = distance(prev_pt, move_point)
        mid_point = tuple(mid_point)
        cv2.circle(image, mid_point, 5, (0, 0, 255), 3)

        if dis > pixel_thresh:
            pyautogui.moveTo(move_point, duration= mouse_duration)
            prev_pt = move_point

        cv2.line(image, pt[0], pt[1], (255, 0, 0), 3)

    if l == 1 and finger_dist < click_thresh :
        move_point = tuple(((pt[0]-np.array((500,170)))*scale))
        dis = distance(prev_pt, move_point)
        now = time.time()
        if not touched:
            touched = True
            start = time.time()
        if now - start > 0.5 :
            if dis < pixel_thresh and (not clicked) and (not mouse_down):
                pyautogui.rightClick()
                clicked = True
                print("Right clicked", finger_dist)
            else :
                if not mouse_down and not clicked: 
                    pyautogui.mouseDown()
                    mouse_down = True
                    print("mouse Down", finger_dist)
        pyautogui.moveTo(move_point, duration=mouse_duration)
        prev_pt = move_point


    # cv2.imshow("mask", mask)
    cv2.imshow("feed", image)

    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()