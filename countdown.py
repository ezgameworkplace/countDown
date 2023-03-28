from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import time
from datetime import datetime, timedelta

class FloatingWindow(QtWidgets.QWidget):

    def __init__(self, parent=None): #TODO 适配多个屏幕
        super(FloatingWindow, self).__init__(parent)
        desktop = QtWidgets.QDesktopWidget()
        screen_number = QtWidgets.QDesktopWidget.screenNumber(desktop)
        screen_resolution = desktop.screenGeometry()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowOpacity(0.5)
        # self.setGeometry(100, 50, 1600, 900)

        self.count_down = QtWidgets.QLabel(self)
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.count_down.setFont(myFont)
        self.count_down.setGeometry(screen_resolution)


        self.count_down.setStyleSheet("color: white; font: 24pt; background-color:transparent")
        self.count_down.setAlignment(QtCore.Qt.AlignHCenter)
        # self.count_down.setAlignment(QtCore.Qt.AlignCenter)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        self.now = datetime.now()
        self.end_time = datetime(2023, 5, 14) # 设置结束日期
        self.rest = self.end_time-self.now
        days, hour_remainder = divmod(int(self.rest.total_seconds()), 86400)
        hours, remainder = divmod(hour_remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.count_down.setText("{}days,{}:{}:{}".format(days, hours, minutes, seconds))



    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FloatingWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
