from GestureController import GestureController
import pyautogui
import time
import cv2

class ZoomControl(GestureController):
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.COOLDOWN = 1.0  # Delay between actions
        self.last_pinch_distance = None  # Tracks the last pinch distance
        self.last_zoom_time = 0  # Time of the last zoom gesture

    def calculate_distance(self, point1, point2):
        """
        Calculate the Euclidean distance between two points.
        """
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def process_gesture(self, fingers, landmarks, frame):
        current_time = time.time()

        # Get the width and height of the frame
        h, w, _ = frame.shape
        thumb_tip = (landmarks[4][0] * w, landmarks[4][1] * h)  # Thumb tip
        index_tip = (landmarks[8][0] * w, landmarks[8][1] * h)  # Index finger tip

        # Calculate the distance between thumb and index finger
        pinch_distance = self.calculate_distance(thumb_tip, index_tip)

        if self.last_pinch_distance is not None:
            # Zoom in (pinch distance increases significantly)
            if pinch_distance > self.last_pinch_distance + 30 and current_time - self.last_zoom_time > self.COOLDOWN:
                pyautogui.hotkey('ctrl', '+')  # Zoom in
                cv2.putText(frame, "Zoom In", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                self.last_zoom_time = current_time

            # Zoom out (pinch distance decreases significantly)
            elif pinch_distance < self.last_pinch_distance - 30 and current_time - self.last_zoom_time > self.COOLDOWN:
                pyautogui.hotkey('ctrl', '-')  # Zoom out
                cv2.putText(frame, "Zoom Out", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.last_zoom_time = current_time

        self.last_pinch_distance = pinch_distance  # Update the last pinch distance
