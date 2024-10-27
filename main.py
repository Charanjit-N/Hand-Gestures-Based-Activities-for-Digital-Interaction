import cv2
import utility
import numpy as np
import pyautogui
# import win32gui
from pynput.mouse import Button, Controller


mouse = Controller()

screen_width , screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

import time  # Import the time module

# Dictionary to track the last activation time for each gesture
last_activation = {
    "up": 0,
    "down": 0,
    "right_click": 0,
    "left_click": 0,
}

# Cooldown time in seconds
COOLDOWN = 1.0  # delay

def detect_gestures(fingers, landmarks, frame):
    current_time = time.time()

    # mouse movement
    if fingers == [0, 1, 1, 0, 0]:
        h, w, c = frame.shape
        x = int(landmarks[8][0] * w)
        y = int(landmarks[8][1] * h)

        xVal = int(np.interp(x, [w//2, 3*w//4], [0, screen_width]))
        yVal = int(np.interp(y, [3*h//8, (5*h)//8], [0, screen_height]))
        # print(w ,h)
        # print(x ,y)
        # print(xVal,yVal)
        pyautogui.moveTo(xVal, yVal)

    # mouse right click
    elif fingers == [1, 1, 0, 0, 0] and current_time - last_activation["right_click"] > COOLDOWN:
        mouse.press(Button.right)
        mouse.release(Button.right)
        cv2.putText(frame, "Right_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        last_activation["right_click"] = current_time
    
    # mouse left click
    elif fingers == [1, 0, 1, 0, 0] and current_time - last_activation["left_click"] > COOLDOWN:
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(frame, "Left_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        last_activation["left_click"] = current_time

    # ppt/pdf previous page (upward arrow keyboard click)
    elif fingers == [1, 0, 0, 0, 0] and current_time - last_activation["up"] > COOLDOWN:
        pyautogui.press("up")
        cv2.putText(frame, "previous_slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_activation["up"] = current_time

    # ppt/pdf next page (downward arrow keyboard click)
    elif fingers == [0, 0, 0, 0, 1] and current_time - last_activation["down"] > COOLDOWN:
        pyautogui.press("down")
        cv2.putText(frame, "next_slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_activation["down"] = current_time

    # Annotation on Document
    # elif fingers == [0,1,0,0,0]:
    #     annotations.append()




def main():
    detector = utility.DetectHand(detectionCon=0.8, maxHands=1)
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)    #3 corresponds to cv2.CAP_PROP_FRAME_WIDTH (frame width)
    cap.set(4, 360)   #4 corresponds to cv2.CAP_PROP_FRAME_HEIGHT (frame height)

    try:
        while cap.isOpened():
            ret,frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame,1)
            hands, frame = detector.findHands(frame)

            if hands:
                hand = hands[0]
                
                fingers = detector.upwardFingers(hand)
                print(fingers)

                landmarks = hand["LM_List"]
                detect_gestures(fingers, landmarks,frame)


            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27 :
                break


    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()