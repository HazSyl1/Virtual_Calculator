import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, frame):
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (225, 255, 225), cv.FILLED)
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (50, 50, 225), 4)
        cv.putText(frame, self.value, (self.pos[0] + 20, self.pos[1] + 50),
                   cv.FONT_HERSHEY_PLAIN, 2, (50, 50, 225), 2)

    def clickCheck(self, x, y, frame):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                         (255, 255, 225), cv.FILLED)
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                         (0, 0, 50), 4)
            cv.putText(frame, self.value, (self.pos[0] + 20, self.pos[1] + 50),
                       cv.FONT_HERSHEY_PLAIN, 2, (50, 50, 25), 6)
            return True
        return False

detect = HandDetector(detectionCon=0.9, maxHands=1)

butListVal = [
    ['1', '2', '3', '+'],
    ['4', '5', '6', '-'],
    ['7', '8', '9', '*'],
    ['0', '/', '.', '=']
]

butList = [Button((x * 100 + 800, y * 100 + 150), 100, 100, butListVal[y][x]) for x in range(4) for y in range(4)]

myEq = ""
delayCounter = 0
finEq = ""


def serve(frame):
    global myEq, delayCounter, finEq
    frame = cv.flip(frame, 1)

    hand, frame = detect.findHands(frame, flipType=False)

    cv.rectangle(frame, (800, 50), (1200, 150), (225, 255, 225), cv.FILLED)
    cv.rectangle(frame, (800, 50), (1200, 150), (50, 50, 225), 4)
    for button in butList:
        button.draw(frame)


    ev=""

    if hand:
        lmList = hand[0]['lmList']
        length, info, frame = detect.findDistance(lmList[8][:2], lmList[12][:2], frame)
        x, y = lmList[8][:2]

        if length < 35:
            for i, button in enumerate(butList):
                if button.clickCheck(x, y, frame) and delayCounter == 0:
                    myVal = butListVal[int(i % 4)][int(i / 4)]
                    if myVal == '=' and myEq != "":
                        finEq = str(eval(myEq))
                        ev=myEq+"="+finEq
                        myEq = ""
                    elif myVal != '=':
                        myEq += myVal
                        finEq = ""
                    delayCounter = 1

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    display_text = finEq if myEq == "" else myEq
    cv.putText(frame, display_text, (820, 114), cv.FONT_HERSHEY_PLAIN, 3, (50, 50, 225), 3)
    if ev!="":
        return frame,ev
    else:
        return frame,""
