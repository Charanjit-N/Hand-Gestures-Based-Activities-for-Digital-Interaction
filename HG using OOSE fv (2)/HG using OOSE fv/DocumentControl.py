from GestureController import GestureController
import pyautogui
import time
import cv2

class DocumentControl(GestureController):
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.COOLDOWN = 1.0  # Delay between actions
        self.last_index_x = None  # Last X position of the index finger
        self.last_swipe_time = 0  # Time of the last swipe gesture

    def process_gesture(self, fingers, landmarks, frame):
        current_time = time.time()

        # Get the width and height of the frame
        h, w, _ = frame.shape
        index_x = int(landmarks[8][0] * w)  # Index finger X position
        index_y = int(landmarks[8][1] * h)  # Index finger Y position

        if self.last_index_x is not None:
            # Swipe left (index finger moves left)
            if index_x < self.last_index_x - 50 and current_time - self.last_swipe_time > self.COOLDOWN:
                pyautogui.press("down")  # Move to next slide
                cv2.putText(frame, "Swipe Left - Next Slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                self.last_swipe_time = current_time

            # Swipe right (index finger moves right)
            elif index_x > self.last_index_x + 50 and current_time - self.last_swipe_time > self.COOLDOWN:
                pyautogui.press("up")  # Move to previous slide
                cv2.putText(frame, "Swipe Right - Previous Slide", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.last_swipe_time = current_time

        self.last_index_x = index_x  # Update the last index position
