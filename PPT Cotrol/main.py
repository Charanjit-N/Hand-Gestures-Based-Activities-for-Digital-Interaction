import cv2
import mediapipe as mp
import pyautogui
import time

def count_raisedFingers(lst) :
    cnt = 0
    threshold = (lst.landmark[0].y*100 - lst.landmark[0].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) >  threshold :
        cnt += 1
    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) >  threshold :
        cnt += 1
    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) >  threshold :
        cnt += 1
    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) >  threshold :
        cnt += 1
    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) >  5 :
        cnt += 1

    return cnt

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands

hand_obj =  hands.Hands(max_num_hands=1)

start_init = False
prev_cnt = -1

while True:
    end_time = time.time()
    _, frm = cap.read()       # 1) ret (or _ in your case): A boolean value indicating whether the frame was successfully read. 2) frame (or frm in your case): The actual frame captured, which is a NumPy array
    frm = cv2.flip(frm,1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]
        cnt = count_raisedFingers(hand_keyPoints)
        if(prev_cnt != cnt):
            if(start_init == False):
                start_time = time.time()
                start_init = True
            elif(end_time - start_time) > 0.2:
                if(cnt==1):
                    pyautogui.press("right")
                elif(cnt==2):
                    pyautogui.press("left")
                elif(cnt==3):
                    pyautogui.press("up")
                elif(cnt==4):
                    pyautogui.press("down")
                elif(cnt==5):
                    pyautogui.press("space")

                prev_cnt = cnt
                start_init = False
        

        drawing.draw_landmarks(frm, hand_keyPoints,hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:    # waitKey(1) : waits for 1 millisec for any press key & ASCII value of ESC is 27
        cv2.destroyAllWindows()
        cap.release()
        break