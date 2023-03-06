import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
#import time

class button:
    def __init__(self,pos,width,height,value):

        self.pos=pos
        self.width=width
        self.height=height
        self.value=value

    def draw(self,frame):

        cv.rectangle(frame, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),
                     (225, 255, 225), cv.FILLED)
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (50, 50, 225), 4  )
        #cv.rectangle(frame, (100, 100), (300, 300), (50, 50, 225), 4)

        cv.putText(frame, self.value, (self.pos[0]+20 , self.pos[1]+50),
                   cv.FONT_HERSHEY_PLAIN, 2, (50, 50, 225), 2)
    def clickCheck(self,x,y):

        #x1 < x < x1+width
        if self.pos[0] < x < self.pos[0] + self.width:
            if self.pos[1] < y < self.pos[1] + self.height:

                cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                             (255, 255, 225), cv.FILLED)
                cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                             (0, 0, 50), 4)
                # cv.rectangle(frame, (100, 100), (300, 300), (50, 50, 225), 4)

                cv.putText(frame, self.value, (self.pos[0] + 20, self.pos[1] + 50),
                           cv.FONT_HERSHEY_PLAIN, 2, (50, 50, 25), 6)
                return True
            else:
                return False





# Webcam
cap = cv.VideoCapture(0)

cap.set(3,1280) #width
cap.set(4,720) #height

detect=HandDetector(detectionCon=0.9,maxHands=1)

#Creating Buttons
butListVal=[ ['1','2','3','+'],
             ['4','5','6','-'],
             ['7','8','9','*'],
             ['0','/','.','=']]

butList=[]
for x in range(4):
    for y in range(4):

        xpos = x*100 +800
        ypos = y*100 +150
        butList.append(button((xpos,ypos),100,100,butListVal[y][x]))

#Variable
myEq= ""
delayCounter =0
finEq=" "
while(True):

    isTrue , frame = cap.read()

    #flipping image
    #0 vertically 1 horizontally
    frame=cv.flip(frame,1)

    #Detection of hand
    hand , frame = detect.findHands(frame, flipType=False)

    #Draw all buttons

    cv.rectangle(frame, (800,50), (800 + 400, 70 + 100),
                 (225, 255, 225), cv.FILLED)
    cv.rectangle(frame, (800,50), (800 + 400, 70 + 100),
                 (50, 50, 225), 4)


    for button in butList:
        button.draw(frame)

    # Checking Hand
    if hand:
        lmList=hand[0]['lmList']
        #lank mark list , has all the points of out fingers

        length,info ,frame=detect.findDistance(lmList[8][:2],lmList[12][:2],frame)
        # 8 is index and 12 is middle
        print(length)
        x, y = lmList[8][:2]

        if length<35:
            for i,button in enumerate(butList):
                if button.clickCheck(x,y) and delayCounter ==0:

                    myVal=(butListVal[int(i%4)][int(i/4)])
                    if(myVal=='='):

                        finEq =str(eval(myEq))
                        myEq=" "
                    else:
                        myEq += myVal
                        finEq=" "
                    delayCounter = 1
                    #time.sleep(0.2)



    #Avoid Duplicates
    if delayCounter != 0:
        delayCounter +=1
        if delayCounter>10:
            delayCounter=0

    # Draw the answerd
    if(myEq==" "):
        cv.putText(frame, finEq, (820, 114 ),
                cv.FONT_HERSHEY_PLAIN, 3, (50, 50, 225), 3)
    else:
        cv.putText(frame, myEq, (820, 114),
                   cv.FONT_HERSHEY_PLAIN, 3, (50, 50, 225), 3)


    #Displaying
    #frame = cv.resize(frame, (900,800), interpolation=cv.INTER_AREA)

    cv.imshow("Live Image",frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows

