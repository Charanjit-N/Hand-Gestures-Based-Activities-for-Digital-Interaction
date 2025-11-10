from GestureController import GestureController
import pyautogui
import time
import cv2
# pyautogui.FAILSAFE = False

class DocumentControl(GestureController):
    def __init__(self):
        pyautogui.FAILSAFE = False

        self.COOLDOWN = 1.0  # delay
        # Variables for tracking swipe gestures based on index finger
        self.last_index_x = None  # Last known X position of the index finger
        self.last_swipe_time = 0  # Last time a swipe gesture was recognized

    def process_gesture(self, fingers, landmarks, frame):
        # global last_index_x, last_swipe_time
        current_time = time.time()

        # Get the width and height of the frame (for gesture calculations)
        h, w, _ = frame.shape  # Ensure h and w are initialized here
        
        # Get the X and Y positions of the index finger tip (landmark index 8)
        index_x = int(landmarks[8][0] * w)
        index_y = int(landmarks[8][1] * h)

        # If index finger displacement is enough to trigger a swipe gesture
        if self.last_index_x is not None:
            # Swipe left to move to the next slide (index finger moves left)
            if index_x < self.last_index_x - 50 and current_time - self.last_swipe_time > self.COOLDOWN:
                pyautogui.press("down")  # Move to next slide
                cv2.putText(frame, "Swipe Left - Next Slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                self.last_swipe_time = current_time

            # Swipe right to move to the previous slide (index finger moves right)
            elif index_x > self.last_index_x + 50 and current_time - self.last_swipe_time > self.COOLDOWN:
                pyautogui.press("up")  # Move to previous slide
                cv2.putText(frame, "Swipe Right - Previous Slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.last_swipe_time = current_time

        # Update the last position of the index finger for the next frame
        self.last_index_x = index_x
        