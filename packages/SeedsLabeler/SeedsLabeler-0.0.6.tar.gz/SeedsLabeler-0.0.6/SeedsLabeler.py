#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import os
import sys
from datetime import datetime
import argparse
import logging
from src.libs.config import CFG

# try:
from PyQt5.QtWidgets import QApplication
# except ImportError:
    # if sys.version_info.major >= 3:
        # import sip
        # sip.setapi('QVariant', 2)
    # from PyQt4.QtCore import QApplication

from src.libs.lib import newIcon
from src.gui.LabelerWindow import LabelerWindow
from src.api.inference_api import InferenceApi


class ActiveImageLabelerWindow(LabelerWindow):

    def __init__(self):
        super(ActiveImageLabelerWindow, self).__init__()

def main():
    '''construct main app and run it'''

    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Image Labeler based on Active Learning")
    parser.add_argument("--host",
                default="127.0.0.1",
                type=str,
                help="host to connect to API")

    parser.add_argument("--port",
                        default=8000,
                        type=int,
                        help="port to connect to API")

    args = parser.parse_args()

    # define logging level (DEBUG/INFO/WARNING/ERROR)
    numeric_level = getattr(logging, CFG.logging.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % CFG.logging.loglevel)

    # set up logging configuration
    os.makedirs(CFG.logging.loggingPath, exist_ok=True)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            # file handler
            logging.FileHandler(
                os.path.join(CFG.logging.loggingPath,
                             datetime.now().strftime('%Y-%m-%d %H-%M-%S.log'))),
            # stream handler
            logging.StreamHandler()
        ])
    # logging.info(f"Running with config:\n{CFG}")

    # create QtApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Seeds Labeler")
    app.setWindowIcon(newIcon("shape_t"))

    # Create GUI
    win = ActiveImageLabelerWindow()
    # Create API
    api = InferenceApi(args.host, args.port)

    # Connect API to GUI
    # GUI detection button connected to API Object Detection
    # (parameter is OpenCV Image)
    win.detect.triggered.connect(lambda: api.detectObjects(win.currentImage.path))

    # API Object Found connected to Window add Shape to current Image
    api.objectFound.connect(win.addShape)
    api.objectsFound.connect(win.addShapes)
    api.errorWithInference.connect(win.errorMessage)

    # Show window and run QtApplication
    win.showMaximized()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())