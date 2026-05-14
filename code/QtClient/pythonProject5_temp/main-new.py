import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from qt_use import Ui_MainWindow
import linkSensor
import matplotlib.animation as animation
from collections import deque
import threading
import time

# 设置服务器和传感器的IP地址和端口
SERVER_IP = '192.168.1.169'
SERVER_PORT = 22009
PACKET_SIZE = 1420  # 单个报文的大小

# 标志位，用于控制线程结束
running = True


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.start_x = None
        self.start_y = None
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            super(MyMainForm, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(MyMainForm, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 5)
        effect_shadow.setBlurRadius(12)
        effect_shadow.setColor(QtCore.Qt.gray)
        widget.setGraphicsEffect(effect_shadow)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainForm()

    screen = QApplication.primaryScreen()
    size = screen.size()
    width, height = size.width(), size.height()
    window_width, window_height = mainWindow.width(), mainWindow.height()
    x = (width - window_width) // 2
    y = (height - window_height) // 2 - 50
    mainWindow.move(x, y)

    mainWindow.setWindowIcon(QIcon("configuration-pic/icon.jpg"))

    mainWindow.show()

    data_queue = deque(maxlen=10000000)  # 使用最大长度maxlen的队列
    data_buffer = deque(maxlen=282 * 116)  # 用于存储282个报文内的数据
    x_range = 27777  # 显示点数

    # 启动服务器线程
    server_socket = linkSensor.start_server(SERVER_IP, SERVER_PORT)

    server_thread = threading.Thread(target=linkSensor.receive_sensor_data, args=(server_socket, data_queue))
    server_thread.daemon = True
    server_thread.start()

    # 设置实时绘图
    axes = mainWindow.wave_widget.fig.subplots(2, 1, sharex=True)
    x = range(x_range)
    x_data = deque([0] * x_range, maxlen=x_range)
    y_data = deque([0] * x_range, maxlen=x_range)

    line_x, = axes[0].plot(x, list(x_data), label='X', linewidth=0.5, color='r')
    line_y, = axes[1].plot(x, list(y_data), label='Y', linewidth=0.5, color='b')

    axes[0].legend()
    axes[1].legend()
    axes[0].set_xlim(0, x_range)
    axes[0].set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    axes[1].set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    axes[0].set_ylabel('Acceleration X (g)')
    axes[1].set_ylabel('Acceleration Y (g)')

    # 设置动画，显式地设置save_count以避免警告，调整interval提高帧率
    ani = animation.FuncAnimation(mainWindow.wave_widget.fig, linkSensor.animate,
                                  fargs=(
                                      data_queue, x_data, y_data, [line_x, line_y], x_range,
                                      data_buffer),
                                  interval=200, save_count=1)
    # ------------------------------------------------------------------
    axes = mainWindow.wave_widget_rul.fig.subplots(2, 1, sharex=True)
    x = range(x_range)
    x_data = deque([0] * x_range, maxlen=x_range)
    y_data = deque([0] * x_range, maxlen=x_range)
    line_x, = axes[0].plot(x, list(x_data), label='X', linewidth=0.5, color='r')
    line_y, = axes[1].plot(x, list(y_data), label='Y', linewidth=0.5, color='b')
    axes[0].legend()
    axes[1].legend()
    axes[0].set_xlim(0, x_range)
    axes[0].set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    axes[1].set_ylim(-1, 1)  # 固定y轴范围在-1g到1g
    axes[0].set_ylabel('Acceleration X (g)')
    axes[1].set_ylabel('Acceleration Y (g)')
    ani00 = animation.FuncAnimation(mainWindow.wave_widget_rul.fig, linkSensor.animate,
                                  fargs=(
                                      data_queue, x_data, y_data, [line_x, line_y], x_range,
                                      data_buffer),
                                  interval=200, save_count=1)

    # 设置关闭事件
    def on_close(event):
        global running
        running = False
        server_socket.close()
        # linkSensor.save_data_to_csv(data_buffer)  # 关闭时保存剩余数据

    mainWindow.wave_widget.fig.canvas.mpl_connect('close_event', on_close)

    # 创建检查并保存数据的线程
    def buffer_check_thread():
        while running:
            linkSensor.check_and_save_data(data_buffer)
            time.sleep(1)  # 每秒钟检查一次缓冲区

    buffer_thread = threading.Thread(target=buffer_check_thread)
    buffer_thread.daemon = True
    buffer_thread.start()

    mainWindow.wave_widget.canvas.draw()
    mainWindow.wave_widget.repaint()

    mainWindow.wave_widget_rul.canvas.draw()
    mainWindow.wave_widget_rul.repaint()


    sys.exit(app.exec_())
