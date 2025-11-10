import cv2
from GestureController import GestureController
from HandDetection import HandDetection

class MainApp:
    def __init__(self):
        self.detector = HandDetection(detectionCon=0.8, maxHands=1)
        
    def start(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 360)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                hands, frame = self.detector.scan_hands(frame)

                if hands:
                    hand = hands[0]
                    fingers = self.detector.upward_fingers(hand)
                    landmarks = hand["LM_List"]

                    GestureController.process_all_gestures(fingers, landmarks, frame)
                
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) == 27:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    app = MainApp()
    app.start()
