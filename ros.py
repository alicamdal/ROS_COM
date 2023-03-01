from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from threading import Thread, Event
from queue import Queue
from time import sleep
from PyQt5.QtGui import QPixmap, QImage
import sys
import cv2


class ROS(QtWidgets.QMainWindow):
    def __init__(self):
        super(ROS, self).__init__()
        uic.loadUi('ros.ui', self)
        self.threadEvent = Event()
        self.threadEvent.clear()
        self.stopFlag = False
        self.btnStart.clicked.connect(self.setEvent)
        self.btnStop.clicked.connect(self.clearEvent)
        Thread(target = self.startStream, args=()).start()
        self.show()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
                self, 'Quit?',
                'Are you sure you want to quit?',
                QtWidgets.QMessageBox.Yes , QtWidgets.QMessageBox.No
            )
        if reply == QtWidgets.QMessageBox.Yes:
            self.stopFlag = True
            event.accept()
        else:
            event.ignore()

    def setEvent(self) -> None:
        self.threadEvent.set()
    
    def clearEvent(self) -> None:
        self.threadEvent.clear()

    def startStream(self) -> None:
        self.cap = cv2.VideoCapture(0)
        while not self.stopFlag:
            if self.threadEvent.is_set():
                ret, self.img = self.cap.read()
                if ret:
                    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                    self.img_h, self.img_w, self.img_c = self.img.shape
                    self.bytesPerLine = self.img_c * self.img_w
                    self.q_image = QImage(self.img.data, self.img_w, self.img_h,self.bytesPerLine, QImage.Format_RGB888)
                    self.imgStreamObj.setPixmap(QPixmap.fromImage(self.q_image))
                sleep(0.050)
            else:
                self.imgStreamObj.clear()
                self.threadEvent.wait(timeout=1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ROS()
    sys.exit(app.exec_())
