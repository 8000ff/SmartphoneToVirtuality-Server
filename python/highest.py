import cv2
import numpy as np

from scipy.signal import convolve2d

from functools import reduce
from operator import and_
from more_itertools import *
from itertools import *


s = [0]

pause = False
caps = [cv2.VideoCapture('video{}.mov'.format(cap)) for cap in s]

u=5
v=3
ux=1
vx=-1
# ux = -1/u**2 - v**2
# vx = 1/v**2
filtre = np.ones((u,u))*ux
start = int((u-v)/2)
end = int(u-(u-v)/2)
filtre[start:end,start:end] = vx

filtre = np.array(
[
    [-1,-1,-1],
    [-1,8,-1],
    [-1,-1,-1]
]
,dtype=float)

nbest = 10



def marker(frame,x,y,z=0,size=2,value=0):
    xcord = list(range(x-size,x+size))
    ycord = list(range(y-size,y+size))
    for point in product(xcord,ycord):
        if point[0]>=0 and point[1]>=0 and point[0]<frame.shape[0] and point[1]<frame.shape[1]:
            frame[point]=value

while reduce(and_,[cap.isOpened() for cap in caps]):
    if not pause:
        frames = [cap.read()[1] for cap in caps]
    for oframe in frames :
    # frames = list(filter(lambda t : t[0]==True,frame))
        frame = oframe
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = frame
        frame = np.array(frame,dtype=float)
        frame /= 255.0 #reduce
        frame -= 0.5 # center

        # print(np.max(frame),np.min(frame),end=" -> ")
        frame = convolve2d(frame,filtre,mode='same')
        amplitude = max(abs(np.min(frame)),np.max(frame))
        frame/=np.sum(np.abs(filtre))
    
    cv2.imshow('frame',frame)

    if mask:= cv2.waitKey(1) & 0xFF:
        if mask == ord('a'):
            frames = [cap.read()[1] for cap in caps]
            # compose = np.hstack(frames)
        if mask == ord('p'):
            pause = not pause
        if mask == ord('q'):
            break