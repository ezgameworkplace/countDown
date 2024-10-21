from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import time
import json
import os
from datetime import datetime, timedelta

# 获取 exe 文件所在目录
if hasattr(sys, '_MEIPASS'):
    # 如果在打包环境中运行，获取 exe 文件所在目录
    base_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# 切换工作目录到 exe 所在的目录
os.chdir(base_path)

# 定义 JSON 文件的路径
json_path = os.path.join(base_path, 'config.json')

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

        # 读取 config.json 中的结束时间
        self.end_time = self.load_end_time_from_config()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def load_end_time_from_config(self):
        # 读取同级目录下的 config.json 文件
        try:
            with open(json_path, "r") as f:
                config = json.load(f)
                # 解析 JSON 中的 end_time
                end_time_str = config.get("end_time")
                return datetime.fromisoformat(end_time_str)
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config: {e}")
            # 如果读取失败，默认设置一个结束日期
            return datetime(2024, 10, 1)

    def update_time(self):
        self.now = datetime.now()
        self.rest = self.end_time - self.now
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
