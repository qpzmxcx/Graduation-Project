from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import serial
import time
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 80, 75, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 130, 75, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 180, 75, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(620, 230, 75, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 30, 75, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(620, 280, 75, 25))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(620, 330, 75, 25))
        self.pushButton_7.setObjectName("pushButton_7")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(40, 450, 700, 100))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(620, 380, 75, 25))
        self.pushButton_8.setObjectName("pushButton_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 信号槽绑定
        self.pushButton_8.clicked.connect(QtWidgets.QApplication.quit)
        self.pushButton_5.clicked.connect(self.communication_test)
        self.pushButton.clicked.connect(self.start_detection)
        self.pushButton_2.clicked.connect(self.stop_detection)
        self.pushButton_3.clicked.connect(self.zoom_in_waveform)
        self.pushButton_4.clicked.connect(self.zoom_out_waveform)
        self.pushButton_6.clicked.connect(self.save_waveform)
        self.pushButton_7.clicked.connect(self.replay_waveform)
        
        # 初始化类属性
        self.ser = None
        self.is_detecting = False
        self.read_timer = QtCore.QTimer()
        self.read_timer.timeout.connect(self.read_serial_data)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "开始检测"))
        self.pushButton_2.setText(_translate("MainWindow", "停止检测"))
        self.pushButton_3.setText(_translate("MainWindow", "放大波形"))
        self.pushButton_4.setText(_translate("MainWindow", "缩小波形"))
        self.pushButton_5.setText(_translate("MainWindow", "通信测试"))
        self.pushButton_6.setText(_translate("MainWindow", "保存波形"))
        self.pushButton_7.setText(_translate("MainWindow", "回放波形"))
        self.pushButton_8.setText(_translate("MainWindow", "退出程序"))

    def communication_test(self):
        ser = serial.Serial(port="COM8",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=0)
        # 发送0x01指令
        ser.write(b'\x01')
        time.sleep(0.5)
        # 读取返回1个字节数据
        reply = ser.read(10)
        print(reply)
        # 如果reply中包含0x00或者0x01，则测试成功
        if b'\x00' in reply or b'\x01' in reply:
            self.textBrowser.append("通信测试成功")
            self.textBrowser.append("串口数据如下：端口号: " + ser.portstr + " 波特率: " + str(ser.baudrate) + " 停止位: " + str(ser.stopbits) + " 校验位: " + str(ser.parity) + " 数据位: " + str(ser.bytesize))
            ser.write(b'\x00')
        else:
            self.textBrowser.append("通信测试失败")
            self.textBrowser.append("返回数据: " + str(reply))
            ser.write(b'\x00')
        ser.close()

    def start_detection(self):
        # 清除文本框
        self.textBrowser.clear()
        # 如果已经在检测中，则直接返回
        if self.is_detecting:
            self.textBrowser.append("已经在检测中...")
            return
            
        try:
            # 创建串口对象
            self.ser = serial.Serial(
                port="COM8",
                baudrate=9600,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                timeout=0
            )
            
            # 发送0x01指令开始数据采集
            self.ser.write(b'\x01')
            
            # 设置检测状态为True
            self.is_detecting = True
            
            # 启动定时器，每100ms读取一次数据
            self.read_timer.start(100)
            
            self.textBrowser.append("开始检测...")
            self.pushButton.setEnabled(False)  # 禁用开始按钮
            self.pushButton_2.setEnabled(True)  # 启用停止按钮
            
        except Exception as e:
            self.textBrowser.append(f"开始检测失败: {str(e)}")
            if self.ser and self.ser.is_open:
                self.ser.close()
                self.ser = None

    def read_serial_data(self):
        """串口数据读取函数，由定时器触发"""
        if not self.ser or not self.is_detecting:
            return
            
        try:
            # 读取可用的串口数据
            if self.ser.in_waiting:
                data = self.ser.read(self.ser.in_waiting)
                if data:
                    # 这里可以处理接收到的数据，比如更新波形图等
                    self.textBrowser.append(f"接收数据: {data.hex()}")
        except Exception as e:
            self.textBrowser.append(f"读取数据错误: {str(e)}")
            self.stop_detection()

    def stop_detection(self):
        # 清除文本框
        self.textBrowser.clear()
        # 停止定时器
        self.read_timer.stop()
        
        # 如果串口已打开，发送停止命令并关闭
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(b'\x00')  # 发送停止命令
                time.sleep(0.1)
                self.ser.close()
            except Exception as e:
                self.textBrowser.append(f"关闭串口错误: {str(e)}")
            finally:
                self.ser = None
        
        # 重置检测状态
        self.is_detecting = False
        
        # 更新UI
        self.textBrowser.append("停止检测")
        self.pushButton.setEnabled(True)   # 启用开始按钮
        self.pushButton_2.setEnabled(False)  # 禁用停止按钮

    def zoom_in_waveform(self):
        pass

    def zoom_out_waveform(self):
        pass

    def save_waveform(self):
        pass

    def replay_waveform(self):
        pass


if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
