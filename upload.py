import threading
import Queue
import time

import logging

class Upload(threading.Thread):
    """docstring for Upload"""
    def __init__(self, name, uplQueue):
        super(Upload, self).__init__()
        self.name = name
        self.mQueue = uplQueue
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
                filePath = self.mQueue.get(True, 0.05)
                logging.info(filePath)
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Upload, self).join(timeout)

    def doUpload(self):
        logging.info('Upload file ')

    def doResume(self):
        logging.info('Resume upload file ')


