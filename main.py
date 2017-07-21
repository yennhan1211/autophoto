import os
import sys
import time

import logging

from camera import Camera
from upload import Upload

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main():

    imgStoreQueue = Queue.Queue()
    smsQueue = Queue.Queue()

    logging.info ('Initializing Camera Module...')

    myCam = Camera('Camera', imgStoreQueue, smsQueue)

    logging.info ('Initializing Upload Module...')

    myUpload = Upload('Upload', imgStoreQueue, smsQueue)

    logging.info ('Initializing SMS Module...')

    logging.info ('App started. Press \'exit\' to quit program.')

    myCam.start()
    myUpload.start()

    while True:
        strInput = raw_input()
        if strInput == 'exit':
            myCam.join()
            myUpload.join()
            break
        else:
            myCam.doCapture()


if __name__ == '__main__':
    main()
