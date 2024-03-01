import cv2 as cv
import pyautogui
import mediapipe as mp

#webcam setup
webcam = cv.VideoCapture(0)
x1 = y1 = x2 = y2 = 0
#hand drawing setup
myHands = mp.solutions.hands.Hands()
drawingUtils = mp.solutions.drawing_utils

while True:
    _,img = webcam.read()
    #flip image
    img = cv.flip(img,1)
    frame_height, frame_width, _ = img.shape
    # convert to rgb
    rgbImage = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # process hand
    output = myHands.process(rgbImage)
    hands = output.multi_hand_landmarks

    '''TODO: {
        create nvidia highlits binds
    }'''

    #volume control
    if hands:
        for hand in hands:
            drawingUtils.draw_landmarks(img, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv.circle(img = img, center=(x,y), radius=5,color=(0,255,255),thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv.circle(img = img, center=(x,y), radius=5,color=(0,0,255),thickness=3)
                    x2 = x
                    y2 = y

        # calculate distance between points to adjust volume
        dist = ((x2-x1) **2 + (y2-y1)**2) ** (0.5) // 4
        print(dist)
        #draw line after capturing points position
        cv.line(img, (x1,y1),(x2,y2),(0,0,0),5)
        if dist > 30:
            pyautogui.press("volumeup")
        elif dist <30 and dist > 20:
            pyautogui.press("volumedown")




    cv.imshow("Hand Detection", img)

    cv.waitKey(10)

    key = cv.waitKey(27)
    if(key == 27):
        break

webcam.release()
cv.destroyAllWindows()

