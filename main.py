#!/usr/bin/env python3
import env
from logging_util import *
import os
import cv2
import time

ARCHIVE_DIR = None

def leftpad(val, desired_length):
    val = str(val)

    while len(val) < desired_length:
        val = '0' + val

    return(val)

def capture():
    cap = cv2.VideoCapture(env.CAMERA_INDEX)
    logger.info('Initiated capture')

    count = 0
    freq = env.CAPTURE_FREQ_SEC

    start_time = time.time()
    last_cap = 0

    while(True):
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        run_time = int(time.time() - start_time)

        if (run_time % freq) == 0:

            if run_time != last_cap:
                count += 1

                filename =  leftpad(count, env.IMAGE_NAME_LENGTH) + '.jpg'
                filepath = ARCHIVE_DIR + filename

                cv2.imwrite(filepath, frame)
                logger.info('Saved image to {}'.format(filepath))

                last_cap = run_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def create_archive_dir():
    if not os.path.isdir(ARCHIVE_DIR):
        logger.info('Creating archive directory at {}'.format(ARCHIVE_DIR))
        os.mkdir(ARCHIVE_DIR)
        logger.info('Archive directory created')

    else:
        logger.info('Archive directory already exists at {}'.format(ARCHIVE_DIR))

def execute():
    global ARCHIVE_DIR

    ARCHIVE_DIR = env.ARCHIVE_DIR
    if ARCHIVE_DIR[-1] != '/':
        ARCHIVE_DIR = ARCHIVE_DIR + '/'

    logger.info('CAMERA_INDEX set to {}'.format(env.CAMERA_INDEX))
    logger.info('ARCHIVE_DIR set to {}'.format(ARCHIVE_DIR))
    logger.info('CAPTURE_FREQ_SEC set to {}'.format(env.CAPTURE_FREQ_SEC))

    create_archive_dir()
    capture()

if __name__ == '__main__':
    execute()
