import os
import subprocess
from threading import Thread

opts = {"fps":30,"ext":".mp4"}
class Recorder(Thread):
    def __init__(self,input):
        Thread.__init__(self)
        self.input = input
        self.output = os.path.basename(input)
    def run(self):
        cmd = "ffmpeg -v warning -an -n -i {} -r {} {}{}".format(self.input,opts["fps"],self.output,opts["ext"])
        print(cmd)
        ret = os.system(cmd)

stream = os.popen('ls -1 /dev/video*')
fd = stream.read().split('\n')
cameras =  []
for path in fd:
    if(path):
        ret = os.system('ffmpeg -v panic -i '+path+' -t 0.5 -f null -')
        if ret == 0:
            cameras.append(path)

recorders = [Recorder(cam) for cam in cameras]
[rec.start() for rec in recorders]