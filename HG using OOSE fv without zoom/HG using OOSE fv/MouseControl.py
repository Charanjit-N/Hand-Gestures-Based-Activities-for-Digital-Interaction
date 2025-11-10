from GestureController import GestureController
import pyautogui
import time
import cv2
import numpy as np
from pynput.mouse import Button, Controller

# mouse = Controller()
# pyautogui.FAILSAFE = False
# screen_width , screen_height = pyautogui.size()

class MouseControl(GestureController):
    def __init__(self):

        self.mouse = Controller()
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()

        self.last_activation = {"right_click": 0, "left_click": 0}
        self.COOLDOWN = 1.0

    def process_gesture(self, fingers, landmarks, frame):
        current_time = time.time()
        # mouse movement
        if fingers == ["R",0, 1, 1, 0, 0]:
            h, w, c = frame.shape
            x = int(landmarks[8][0] * w)
            y = int(landmarks[8][1] * h)

            xVal = int(np.interp(x, [w//2, 3*w//4], [0, self.screen_width]))
            yVal = int(np.interp(y, [3*h//8, (5*h)//8], [0, self.screen_height]))
            pyautogui.moveTo(xVal, yVal)
        elif fingers==["L",0,0,1,1,0]:
            h, w, c = frame.shape
            x = int(landmarks[8][0] * w)
            y = int(landmarks[8][1] * h)

            xVal = int(np.interp(x, [w//4,w//2], [0, self.screen_width]))
            yVal = int(np.interp(y, [3*h//8, (5*h)//8], [0, self.screen_height]))
            pyautogui.moveTo(xVal, yVal)

        # mouse left click
        elif fingers == ["R",1, 0, 1, 0, 0] or fingers == ["L",0,0,0,1,1] and current_time - self.last_activation["left_click"] > self.COOLDOWN:
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            cv2.putText(frame, "Left_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.last_activation["left_click"] = current_time

        # mouse right click
        elif fingers == ["R",1, 1, 0, 0, 0] or fingers == ["L",0,0,1,0,1] and current_time - self.last_activation["right_click"] > self.COOLDOWN:
            self.mouse.press(Button.right)
            self.mouse.release(Button.right)
            cv2.putText(frame, "Right_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self.last_activation["right_click"] = current_time

      
        
