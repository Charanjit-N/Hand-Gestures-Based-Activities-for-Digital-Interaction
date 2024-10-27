import mediapipe as mp
import cv2

class DetectHand:

    def __init__(self, staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.staticMode,
                                        max_num_hands=self.maxHands,
                                        model_complexity=modelComplexity,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []


    
    def findHands(self, frame, draw=True, flip = True):
        
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        allHands =[]
        height, width, channels = frame.shape

        if self.results.multi_hand_landmarks:
            for handType, handLandmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                hand = {}
                landmarksList = []
                x_values =[]
                y_values =[]
                for id, lm in enumerate(handLandmarks.landmark):
                    px, py , pz = int(lm.x * width), int(lm.y * height),int(lm.z * width)
                    # landmarksList.append([px, py,pz])
                    landmarksList.append([lm.x,lm.y,lm.z])
                    x_values.append(px)
                    y_values.append(py)

                # for drawing bounding box
                x_min, x_max = min(x_values), max(x_values)
                y_min, y_max = min(y_values), max(y_values)
                box_width, box_height = (x_max - x_min) , (y_max - y_min)
                box = x_min, y_min, box_width,box_height
                center_x, center_y = box[0] + (box[2] // 2), box[1] + (box[3] // 2)

                hand["LM_List"] = landmarksList
                hand["bbox"] = box
                hand["center"] = (center_x, center_y)

                if flip:
                    if handType.classification[0].label == "Right":
                        hand["type"] = "Right"
                    else:
                        hand["type"] = "Left"
                # else:
                #     hand["type"] = handType.classification[0].label

                allHands.append(hand)

                if draw:
                    self.mpDraw.draw_landmarks(frame, handLandmarks,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(frame, (box[0] - 20, box[1] - 20),
                                  (box[0] + box[2] + 20, box[1] + box[3] + 20),
                                  (0, 0, 255), 2)
                    cv2.putText(frame, hand["type"], (box[0] - 30, box[1] - 30), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 0, 0), 2)
                    
        return allHands, frame
    

    def upwardFingers(self, hand):

        fingers = []
        handType = hand["type"]
        landmarksList = hand["LM_List"]
        if self.results.multi_hand_landmarks:

            # For Thumb Finger
            if handType == "Right":
                if landmarksList[self.tipIds[0]][0] < landmarksList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if landmarksList[self.tipIds[0]][0] > landmarksList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # For four other Fingers
            for id in range(1, 5):
                if landmarksList[self.tipIds[id]][1] < landmarksList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers


def main():

    cap = cv2.VideoCapture(0)
    detector = DetectHand(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    while True:
        ret_bool, frame = cap.read()
        frame = cv2.flip(frame,1)

        hands, frame = detector.findHands(frame, draw=True,flip=True)

        if hands:
            hand1 = hands[0]
            landmarksList1 = hand1["LM_List"]
            box1 = hand1["bbox"]
            center1 = hand1["center"]
            handType1 = hand1["type"]
            
            upFingers1 = detector.upwardFingers(hand1)
            print(f"---->{upFingers1}")

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == 27 :
            break

            
if __name__ == "__main__":
    main()