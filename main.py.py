import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Parameters
width, height = 640, 480  # Reduced window size
gestureThreshold = 150
folderPath = r"C:\Users\chara\OneDrive\Desktop\Slides"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(10, width)
cap.set(10, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
delay = 10  # Reduced delay for faster responsiveness
buttonPressed = False
counter = 0
imgNumber = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(60), int(106)  # Smaller size for the smaller image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Load images initially to avoid repeated I/O operations
imgList = [cv2.resize(cv2.imread(os.path.join(folderPath, img)), (width, height)) for img in pathImages]

while True:
    
    # Get image frame
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw

    # Draw Gesture Threshold line on the image window
    #cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 3)

    # Get the current slide image
    imgCurrent = imgList[imgNumber].copy()

    if hands and not buttonPressed:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [100, height-100], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 6, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 6, (0, 0, 255), cv2.FILLED)
        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # Draw annotations on the current slide image
    for annotation in annotations:
        for j in range(1, len(annotation)):
            cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 6)

    # Resize the webcam image and overlay it on the slide image
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    # Display the windows
    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
