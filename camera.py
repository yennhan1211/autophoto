import threading
import Queue
import time

import logging

class Camera(threading.Thread):
    """docstring for Camera"""
    def __init__(self, name, imgQueue):
        super(Camera, self).__init__()
        self.name = name
        self.mQueue = imgQueue
        self.stoprequest = threading.Event()

    def setLog(self):
        pass

    def run(self):
        i = 0
        while not self.stoprequest.isSet():
            self.mQueue.put('element ' + str(i))
            i += 1
            time.sleep(1)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Camera, self).join(timeout)

    def doCapture(self):
        logging.info('Trigger capture')

    def doSleep(self):
        logging.info('Trigger Sleep')
