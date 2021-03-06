import cv2
from VideoCaptureAsync import VideoCaptureAsync

import numpy as np
from math import *

from operator import and_
from functools import reduce
from itertools import *
from more_itertools import *

import argparse

from time import time
def delta_time():
    return difference(repeatfunc(time),initial=time())
def avg(g,n=10):
    from collections import deque
    last = deque(maxlen=n)
    while True:
        last.append(next(g))
        yield np.mean(last)
def printEvery(g,n=20):
    i=0
    while i := i+1 :
        value = next(g)
        if i%n==0:
            print(value)
        yield value


parser = argparse.ArgumentParser(description='Track the highest value point in videos.')
parser.add_argument('inputs', type=str, nargs='+',default=['/dev/video{}'.format(x) for x in [0,2,4]])
parser.add_argument('--shrink', type=int,default=1)
parser.add_argument('--width',type=int,default=640)
parser.add_argument('--height',type=int,default=360)
parser.add_argument('--framerate',type=int,default=20)
parser.add_argument('--xtile',type=int,default=1)
parser.add_argument('--oversample',type=int,default=4)
parser.add_argument('--mask',type=int,default=16)

args = parser.parse_args()
print(args)

# Prints the average frametime over time
avgdt = printEvery(avg(delta_time()),args.framerate)


tflip = lambda a,b : (b,a)
shrink = lambda h,w : (int(h/args.shrink),int(w/args.shrink))
print(shrink(args.height,args.width))
shrinkFrame = lambda frame : cv2.resize(frame,tflip(*shrink(*frame.shape[:2])))

fillvalue = np.zeros((*shrink(args.height,args.width),3),dtype=np.uint8)

VCA = lambda input: VideoCaptureAsync(input,args.width,args.height,args.framerate,args.oversample)
caps = [VCA(input) for input in args.inputs]
for cap in caps:
    cap.start()

# build the hitboxes for each view
hbx = []
for y in range(ceil(len(caps)/2)):
    for x in range(args.xtile):
        hbx.append((x*args.width,y*args.height))
# removes empty views
hbx = hbx[:len(caps)]

print(hbx)

lasts = [None] * len(caps)

def dist_mask(shape,center):
    X, Y = np.ogrid[:shape[0], :shape[1]]
    return np.sqrt((X - center[0])**2 + (Y-center[1])**2)

def marker(frame,point,z=0,size=2,value=0):
    frame[dist_mask(frame.shape,point) <= size] = value

def register(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        for box,i in zip(param,range(len(param))):
            bx,by = shrink(*box)
            w,h = shrink(args.width,args.height)
            # inside rectangle
            if bx<x<(bx+w) and by<y<(by+h):
                if event == cv2.EVENT_LBUTTONDOWN:
                    # remap window coordinate to data ones
                    lasts[i] = (args.shrink*(y-by),args.shrink*(x-bx) )
                if event == cv2.EVENT_RBUTTONDOWN:
                    lasts[i] = None

def deform(frame):
    return np.sum(frame,axis=-1) / (255.0 * 3)

def find(frame,last):
    dmask = dist_mask(frame.shape,last)
    cmask = dmask <= args.mask
    hyp = np.max(dmask)

    # Absolutly limits the distance between two consecutive matchs
    frame[~cmask] = 0
    # Makes the pixel values proportional to their distance from the last match
    frame -= dmask/hyp
    # Take the highest one
    return np.unravel_index(frame.argmax(),frame.shape)

# Read the first frame of each capture
acks,frames = list(zip(*(cap.read() for cap in caps)))

while reduce(and_,acks) and next(avgdt):

    displayed = [None] * len(caps)

    # Read frames
    acks,frames = zip(*(cap.read() for cap in caps))

    for i, frame, last in zip( count(), frames, lasts ):
        displayed[i] = shrinkFrame(frame.copy())
        if last:
            # Find the new best match
            lasts[i] = find(deform(frame),last)
            marker(displayed[i],(shrink(*lasts[i])),size=5,value=(255,0,0))

    # Puts the images in a grid
    compose = np.vstack([np.hstack(group) for group in grouper(displayed,args.xtile,fillvalue)])

    cv2.imshow('frame',compose)

    cv2.setMouseCallback('frame',register,param=hbx)
    if mask:= cv2.waitKey(1) & 0xFF:
        if mask == ord('q'):
            break

for cap in caps:
    cap.stop()