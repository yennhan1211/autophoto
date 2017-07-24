import os
import sys
import subprocess
import threading
import Queue
import time

import logging

GPHOTO_PATH     = "gphoto2"
DETECT          = "--auto-detect"
CAPTURE         = "--capture-image-and-download"
FILENAME        = "--filename"

FILEPATH        = "%Y%m%d-%H%M%S.jpg"

PROCESS_FOLDER  = "imgStore"
META_FILE       = "meta.txt"

class Camera(threading.Thread):
    """docstring for Camera"""
    def __init__(self, name, imgQueue, smsQueue):
        super(Camera, self).__init__()
        self.name = name
        self.mImgQueue = imgQueue
        self.mSmsQueue = smsQueue
        self.stoprequest = threading.Event()
        self.triggerInterval = 60 # 600s
        self.defaultPath = os.getcwd()

    def setInterval(self, interval):
        self.triggerInterval = interval

    def setLog(self):
        pass

    def setSaveLocation(self, path):
        self.defaultPath = path

    def run(self):
        os.chdir(self.defaultPath)

        metaFilePath = os.path.join(self.defaultPath, META_FILE )
        processFolderPath = os.path.join(self.defaultPath, PROCESS_FOLDER)

        fileUploaded = []

        if os.path.exists(metaFilePath):
            fileUploaded = open(metaFilePath, 'rb').readlines()

        if not os.path.exists(processFolderPath):
            logging.info ('Create folder')
            os.makedirs(processFolderPath)

        for root, dirs, files in os.walk(PROCESS_FOLDER):
            for filename in files:
                tmpPath = os.path.join(root, filename)
                if tmpPath not in fileUploaded:
                    self.mImgQueue.put(tmpPath)

        while not self.stoprequest.isSet():
            if self.doCheckCamera():
                imgPath, ret = self.doCapture()
                if ret:
                    self.mImgQueue.put(imgPath)
            time.sleep(self.triggerInterval)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Camera, self).join(timeout)

    def doCapture(self):
    # New file is in location /capt0000.jpg on the camera
    # Saving file as capt0000.jpg
    # Deleting 'capt0000.jpg' from folder '/'...
    # Deleting file /capt0000.jpg on the camera
        logging.info('Trigger capture')

        imgPath = ''
        retVal = False
        out, err = runCommand([GPHOTO_PATH, CAPTURE, FILENAME, (self.defaultPath + '/%Y%m%d-%H%M%S.jpg')])

        if err is None and out is not None:
            if 'Error' not in out:
                result = out.strip().split('\n')
                if 'Saving file as' in result[1]:
                    retVal = True
                    imgPath = result[1].replace('Saving file as', '').strip()
                    logging.info(result[1])
            else:
                imgPath = 'Error'
        return imgPath, retVal

    def doCheckCamera(self):
    # Model                          Port
    # ----------------------------------------------------------
    # Nikon DSC D7000 (PTP mode)     usb:001,005
        logging.info('Checking camera')
        retVal = False
        out, err = runCommand([GPHOTO_PATH, DETECT])

        if err is None:
            result = out.strip().split('\n')
            if len(result) > 2:
                retVal = True
                logging.info('Found camera:')
                for s in result[2:]:
                    logging.info(s)
            else:
                logging.info('Camera not found')

        return retVal

def runCommand(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)

    out, err = proc.communicate()

    if out is not None:
        logging.debug (out)
    if err is not None:
        logging.debug (err)

    return out, err

if __name__ == '__main__':
    imgStoreQueue = Queue.Queue()
    smsQueue = Queue.Queue()
    cam = Camera('Camera', imgStoreQueue, smsQueue)
    cam.setSaveLocation('/home/pi')
    if cam.doCheckCamera():
        cam.doCapture()
        print ('Found')
    else:
        print ('Not Found')

