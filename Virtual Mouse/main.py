import cv2
import mediapipe as mp
import pyautogui
import util
from pynput.mouse import Button, Controller
import random


screen_width , screen_height = pyautogui.size()
mouse = Controller()

mpHands = mp.solutions.hands
hand =  mpHands.Hands(
        # static_image_model = False,
        model_complexity = 1,
        min_detection_confidence =0.7,
        min_tracking_confidence = 0.7,
        max_num_hands=1
    )

def find_finger_tip(processed_hand):
    if processed_hand.multi_hand_landmarks:
            hand_landmarks = processed_hand.multi_hand_landmarks[0]
            return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x *screen_width )
        y = int(index_finger_tip.y *screen_height )
        pyautogui.moveTo(x,y)

def is_left_click(landmarks_list, thumb_index_distance):
    return (
            util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            thumb_index_distance > 50
    )


def is_right_click(landmarks_list, thumb_index_distance):
    return (
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90  and
            thumb_index_distance > 50
    )


def is_double_click(landmarks_list, thumb_index_dist):
    return (
            util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_dist > 50
    )


def is_screenshot(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
    )


def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        # print(index_finger_tip)

        thumb_index_distance = util.get_distance([landmarks_list[4],landmarks_list[5]])
        if thumb_index_distance<50 and util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])>90:
            move_mouse(index_finger_tip)

        # LEFT_CLICK
        elif is_left_click(landmarks_list,  thumb_index_distance):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # RIGHT_CLICK
        elif is_right_click(landmarks_list, thumb_index_distance):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # DOUBLE_CLICK
        elif is_double_click(landmarks_list, thumb_index_distance):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double_Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        #SCREEN_SHOT
        elif is_screenshot(landmarks_list,thumb_index_distance ):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            # im1.save(f'my_screenshot_{label}.png')
            im1.save(f'C:/Users/chara/OneDrive/Desktop/my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot_Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)







def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret,frame = cap.read()

            if not ret:
                break
            frame =cv2.flip(frame,1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_hand  = hand.process(frameRGB)

            landmarks_list = []

            if processed_hand.multi_hand_landmarks:
                hand_landmarks = processed_hand.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x,lm.y))
                # print(landmarks_list, end ='\n')

                detect_gestures(frame, landmarks_list, processed_hand)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == 27 :
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
            
