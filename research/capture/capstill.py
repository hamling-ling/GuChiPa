import cv2
import threading
import time
import datetime
import getch as mg
import sys
import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

class CvThread(threading.Thread):

    def __init__(self):
        super(CvThread, self).__init__()
        self.isStopped = False
        
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened() is False:
            raise("IO Error")

        cv2.namedWindow("Capture", cv2.WINDOW_NORMAL)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
        self.cmd = ""
        self.lock = threading.Lock()

    def run(self):
        while(self.isStopped == False):
            ret, image = self.cap.read()

            if ret == False:
                continue
            
            height = image.shape[0]
            width = image.shape[1]

            edge_len = int(height * 0.8)
            ori = (int((width - edge_len)/2), int((height-edge_len)/2))
            cv2.rectangle(image, ori, (ori[0]+edge_len, ori[1]+edge_len), (255, 0, 0), 4)

            cv2.imshow("Capture", image)
            
            cmd = self.getCmd()
            if(cmd != ""):
                self.still(cmd, image)
                self.setCmd("")
        cv2.destroyAllWindows()

    def getCmd(self):
        with self.lock:
            return self.cmd

    def setCmd(self, cmd):
        with self.lock:
            self.cmd = cmd
 
    def still(self, cmd, image):
        
        if cmd != "g" and cmd != "c" and cmd != "a":
            print("not recognized:" + cmd)
            return

        now = datetime.datetime.now()
        file = now.strftime("%Y%m%d_%H%M%S") + ".png"
        dir = cmd
        make_sure_path_exists(dir)
        fullname = dir + '/' + file

        cv2.imwrite(fullname, image)
        print("saved " + fullname)

    def stop(self):
        self.isStopped = True

if __name__ == '__main__':

    th_cl = CvThread()
    th_cl.start()

    print("press q to quit")

    while(True):
        ch = mg.getch()
        sys.stdout.flush()
        
        if(ch == 'q') :
            th_cl.stop()
            break
        th_cl.setCmd(ch)

    th_cl.join()
