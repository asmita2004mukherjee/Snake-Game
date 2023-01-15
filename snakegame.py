import cvzone
import math
import random
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)


class snakegame:
    def __init__(self,pathFood):
        self.points = []
        self.lengths = []
        self.currentlength = 0
        self.allowedlength = 150
        self.previoushead = 0,0
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(25, 100), random.randint(50, 75)

    def update(self,imgMain,headcurrent):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)


        px, py = self.previoushead
        cx, cy = headcurrent

        self.points.append([cx, cy])
        distance = math.hypot(cx -px ,cy-py)
        self.lengths.append(distance)
        self.currentlength += distance
        self.previoushead =cx,cy
        #length reduction

        if self.currentlength>self.allowedlength:
            for i,length in enumerate(self.lengths):

                self.currentlength -=length
                self.lengths.pop(i)
                self.points.pop(i)#yeh isliye kiya kyuki stack se bhi toh niklana hai
                if self.currentlength < self.allowedlength:
                    break
        #check if snake ate the food just checks if our finger is in the recangular refion
        rx, ry = self.foodPoint
        if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                ry - self.hFood // 2 < cy < ry + self.hFood // 2:
            print("ate")
            self.randomFoodLocation()
            self.allowedlength += 50
            self.score += 1
            print(self.score)

        #check for collison
        pts = np.array(self.points[:-2], np.int32)#formlimity to convert to np
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)




        #draw snake
        if self.points: #index out range error hatane ke liye

            for i,point in enumerate(self.points):

                if i!=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)

            cv2.circle(imgMain, self.points[-1], 20, (2000, 0, 200), cv2.FILLED)#index ki jaga last pont hai -1 wlala

            # draw food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
            # check for collison after drawing cuz u know hari line aayegi
            pts = np.array(self.points[:-2], np.int32)  # formlimity to convert to np
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

            if -1 <= minDist <= 1: #range cuz 0 nahi dega exact har baar
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()
                self.score = 0







        return imgMain
game = snakegame(r"C:\Users\asmit\OneDrive\Documents\DOCW\donut.jpg")


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)# 1 matlab horizontal axis
    hands,img = detector.findHands(img,flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)


    cv2.imshow("image",img)
    cv2.waitKey(1)
