# -*- coding: utf-8 -*-

# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py

from Module import iface, eapol
import os
import threading


from PyQt5 import QtCore, QtGui, QtWidgets


def check_su():
    if os.getuid() == 0:
        return True
    else:
        return False


super_user = check_su()

status_monitor = False



def set_mode(intface,mode,gui):
	error_massege = ['Error','error','Failed','failed','not','Not']
	s_result = ''
	try:
		if mode == 0:
			gui.console.append(f'[InterFace] {intface} down')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} down').read()
			gui.console.append(f'[InterFace] Set {intface} Managed mode')
			s_result = s_result + ' ' + os.popen(f'iwconfig {intface} mode managed').read()
			gui.console.append(f'[InterFace] {intface} up')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} up').read()
			gui.console.append(f'[InterFace] Successfully Change Mode')
			if s_result in error_massege:
				return False
			return True
		elif mode == 1:
			gui.console.append(f'[InterFace] {intface} down')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} down').read()
			gui.console.append(f'[InterFace] Set {intface} Monitor mode')
			s_result = s_result + ' ' + os.popen(f'iwconfig {intface} mode monitor').read()
			gui.console.append(f'[InterFace] {intface} up')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} up').read()
			gui.console.append(f'[InterFace] Successfully Change Mode')
			if s_result in error_massege:
				return False
			return True
	except Exception as ex_m:
		return ex_m
	


class Ui_Form(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1280, 720)
		MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
		MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.background = QtWidgets.QLabel(self.centralwidget)
		self.background.setGeometry(QtCore.QRect(0, 0, 1280, 720))
		self.background.setText("")
		self.background.setPixmap(QtGui.QPixmap("GUI/GUI.jpg"))
		self.background.setObjectName("background")
		self.button_minimize = QtWidgets.QPushButton(self.centralwidget)
		self.button_minimize.setGeometry(QtCore.QRect(1179, 0, 51, 51))
		self.button_minimize.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_minimize.setText("")
		self.button_minimize.setObjectName("button_minimize")
		self.button_exit = QtWidgets.QPushButton(self.centralwidget)
		self.button_exit.setGeometry(QtCore.QRect(1229, 0, 51, 51))
		self.button_exit.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_exit.setText("")
		self.button_exit.setObjectName("button_exit")
		self.button_monitor = QtWidgets.QPushButton(self.centralwidget)
		self.button_monitor.setGeometry(QtCore.QRect(40, 160, 40, 20))
		self.button_monitor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_monitor.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("GUI/off.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.button_monitor.setIcon(icon)
		self.button_monitor.setIconSize(QtCore.QSize(40, 20))
		self.button_monitor.setCheckable(False)
		self.button_monitor.setChecked(False)
		self.button_monitor.setObjectName("button_monitor")
		self.button_connection = QtWidgets.QPushButton(self.centralwidget)
		self.button_connection.setGeometry(QtCore.QRect(40, 240, 40, 20))
		self.button_connection.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_connection.setText("")
		self.button_connection.setIcon(icon)
		self.button_connection.setIconSize(QtCore.QSize(40, 20))
		self.button_connection.setCheckable(False)
		self.button_connection.setChecked(False)
		self.button_connection.setObjectName("button_connection")
		self.button_WS = QtWidgets.QPushButton(self.centralwidget)
		self.button_WS.setGeometry(QtCore.QRect(470, 110, 40, 20))
		self.button_WS.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_WS.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("GUI/off_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.button_WS.setIcon(icon1)
		self.button_WS.setIconSize(QtCore.QSize(40, 20))
		self.button_WS.setCheckable(False)
		self.button_WS.setChecked(False)
		self.button_WS.setObjectName("button_WS")
		self.button_CW = QtWidgets.QPushButton(self.centralwidget)
		self.button_CW.setGeometry(QtCore.QRect(470, 310, 40, 20))
		self.button_CW.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_CW.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("GUI/off_green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.button_CW.setIcon(icon2)
		self.button_CW.setIconSize(QtCore.QSize(40, 20))
		self.button_CW.setCheckable(False)
		self.button_CW.setChecked(False)
		self.button_CW.setObjectName("button_CW")
		self.button_BF = QtWidgets.QPushButton(self.centralwidget)
		self.button_BF.setGeometry(QtCore.QRect(470, 510, 40, 20))
		self.button_BF.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_BF.setText("")
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap("GUI/off_orange.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.button_BF.setIcon(icon3)
		self.button_BF.setIconSize(QtCore.QSize(40, 20))
		self.button_BF.setCheckable(False)
		self.button_BF.setChecked(False)
		self.button_BF.setObjectName("button_BF")
		self.button_anti_jamming = QtWidgets.QPushButton(self.centralwidget)
		self.button_anti_jamming.setGeometry(QtCore.QRect(730, 150, 40, 20))
		self.button_anti_jamming.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_anti_jamming.setText("")
		self.button_anti_jamming.setIcon(icon)
		self.button_anti_jamming.setIconSize(QtCore.QSize(40, 20))
		self.button_anti_jamming.setCheckable(False)
		self.button_anti_jamming.setChecked(False)
		self.button_anti_jamming.setObjectName("button_anti_jamming")
		self.console = QtWidgets.QTextEdit(self.centralwidget)
		self.console.setGeometry(QtCore.QRect(860, 80, 380, 600))
		self.console.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
		self.console.setObjectName("console")
		self.line_monitor = QtWidgets.QTextEdit(self.centralwidget)
		self.line_monitor.setGeometry(QtCore.QRect(40, 120, 200, 30))
		self.line_monitor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_monitor.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.line_monitor.setObjectName("line_monitor")
		self.line_adaptor = QtWidgets.QTextEdit(self.centralwidget)
		self.line_adaptor.setGeometry(QtCore.QRect(40, 300, 200, 30))
		self.line_adaptor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_adaptor.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.line_adaptor.setObjectName("line_adaptor")
		self.line_password = QtWidgets.QTextEdit(self.centralwidget)
		self.line_password.setGeometry(QtCore.QRect(40, 370, 200, 30))
		self.line_password.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_password.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.line_password.setObjectName("line_password")
		self.line_eapol = QtWidgets.QTextEdit(self.centralwidget)
		self.line_eapol.setGeometry(QtCore.QRect(450, 150, 41, 21))
		self.line_eapol.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_eapol.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.line_eapol.setObjectName("line_eapol")
		self.line_thread = QtWidgets.QTextEdit(self.centralwidget)
		self.line_thread.setGeometry(QtCore.QRect(450, 180, 41, 21))
		self.line_thread.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_thread.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.line_thread.setObjectName("line_thread")
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.console.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


class MyWindow(QtWidgets.QMainWindow, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.button_minimize.clicked.connect(self.minimize)
		self.button_exit.clicked.connect(self.exit)

		self.button_monitor.clicked.connect(self.on_monitor)

		self.button_minimize.setStyleSheet(
			'''
			QPushButton{background-color: rgba(255,255,255,0);border: 0px;}
			QPushButton:hover{background-color: rgba(39, 39, 39, 100);}
			'''
		)

		self.button_exit.setStyleSheet(
			'''
			QPushButton{background-color: rgba(255,255,255,0);border: 0px;}
			QPushButton:hover{background-color: rgba(39, 39, 39, 100);}
			'''
		)
		
		if iface.default_if() != None:
			self.line_monitor.setText(iface.default_if())

			if iface.check_monitor(self.line_monitor.toPlainText()):
				global status_monitor
				adapter_name = self.line_monitor.toPlainText()
				status_monitor = True
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("GUI/on.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.button_monitor.setIcon(icon)
				self.console.append(f'[IDzone] Wireless Adapter {adapter_name} is set to Monitor')
		else:
			self.line_monitor.setText('')
			
		if not super_user:
			self.console.append('[WARNING] Not a SuperUser. Please run it with admin privileges')


	def minimize(self):
		self.showMinimized()

	def exit(self):
		sys.exit(app.exec_())



	def center(self):
		qr = self.frameGeometry()
		cp = QtCore.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		delta = QtCore.QPoint(event.globalPos() - self.oldPos)
		self.move(self.x() + delta.x(), self.y() + delta.y())
		self.oldPos = event.globalPos()


	def on_monitor(self):
		if super_user:
			global status_monitor
			adapter_name = self.line_monitor.toPlainText()
			if iface.check_if(adapter_name):
				if status_monitor == True:
					f_result = set_mode(adapter_name,0,self)
					if f_result == True:
						status_monitor = False
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap("GUI/off.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
						self.button_monitor.setIcon(icon)
						self.console.append(f'[IDzone] Wireless Adapter {adapter_name} is set to Managed Mode')
					else:
						self.console.append(f'[IDzone] Faild to change {adapter_name} mode : {f_result}')
				else:
					f_result = set_mode(adapter_name,1,self)
					if f_result == True:
						status_monitor = True
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap("GUI/on.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
						self.button_monitor.setIcon(icon)
						self.console.append(f'[IDzone] Wireless Adapter {adapter_name} is set to Monitor Mode')
					else:
						self.console.append(f'[IDzone] Faild to change {adapter_name} mode : {f_result}')
			else:
				self.console.append(f'[IDzone] Invailed Wireless Adapter Name')
		else:
			self.console.append('[WARNING] Not a SuperUser. Please run it with admin privileges')
		
	


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	myWindow = MyWindow()
	myWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	myWindow.show()
	sys.exit(app.exec_())
	MainWindow.show()
	sys.exit(app.exec_())
