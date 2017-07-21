import os
import sys
import subprocess
import threading
import Queue
import time

import logging

GPHOTO_PATH     = 'fart.exe'
DETECT          = '--auto-detect'
CAPTURE         = '--capture-image-and-download'
FILENAME        = '--filename'

FILEPATH        = '%s-%Y%m%d-%H%M%S.jpg'

class Camera(threading.Thread):
    """docstring for Camera"""
    def __init__(self, name, imgQueue, smsQueue):
        super(Camera, self).__init__()
        self.name = name
        self.mImgQueue = imgQueue
        self.mSmsQueue = smsQueue
        self.stoprequest = threading.Event()
        self.triggerInterval = 600 # 600s

    def setInterval(self, interval):
        self.triggerInterval = interval

    def setLog(self):
        pass

    def run(self):
        i = 0
        while not self.stoprequest.isSet():
            self.mImgQueue.put('element ' + str(i))
            i += 1
            time.sleep(self.triggerInterval)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Camera, self).join(timeout)

    def doCapture(self):
        logging.info('Trigger capture')

        imgPath = ''
        retVal = False
        out, err = runCommand([GPHOTO_PATH, CAPTURE, FILENAME, (FILEPATH)])

        if err == None:
            result = out.split('\n')

        return imgPath, retVal

    def doCheckCamera(self):
        logging.info('Checking camera')

def runCommand(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)

    out, err = proc.communicate()

    if out != None:
        logging.debug (out)
    if err != None:
        logging.debug (err)

    return out, err

if __name__ == '__main__':
    runCommand([GPHOTO_PATH, "--help"])
