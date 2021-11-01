# -*- coding: utf-8 -*-

# python -m PyQt5.uic.pyuic -x untitled.ui -o test-gui.py

from Module import iface
from scapy.all import *
import os
import threading
import random
import time


from PyQt5 import QtCore, QtGui, QtWidgets

# GLOBAL SETTINGS =====================================================================

GLOBAL_GUI = 0
GLOBAL_WIRELESS_PROTECTOR = True

status_monitor = False

GLOBAL_IFACE = ''

GLOBAL_INDICATE = {'scan':False,'channel_hop':False,'sniff_protector':[False,False]}

#======================================================================================

# WiFi Scanner=========================================================================
ap_list = []

scan_gui = ''

def scan_handler(packet):
	global ap_list
	if packet.haslayer(Dot11):
		if packet.type == 0 and packet.subtype == 8:
			offset = 16*3+8+6
			raw_pkt = bytes(packet)
			length = raw_pkt[offset-1]
			SSID = raw_pkt[offset:offset+length]
			channel = raw_pkt[offset+length+12]
			if not b'\x00' in SSID:
				if not SSID == b'':
					print_line = f'{len(ap_list)+1}. {SSID} - {channel}'
					if not print_line in ap_list:
						ap_list.append(print_line)


S
def start_scan(gui):
	global ap_list
	global scan_gui
	ap_list = []
	scan_gui = gui
	ch_list = [1,3,7,11]
	for i in ch_list:
		sniff(prn=scan_handler, timeout=1.5, iface=GLOBAL_IFACE)
		os.system(f'sudo iwconfig {GLOBAL_IFACE} channel {i}')
		GLOBAL_INDICATE['channel_hop'] = i
	GLOBAL_INDICATE['scan'] = True

#======================================================================================

# Wireless Sniff Protector ============================================================

eapol_sample_1 = b'\x00\x00\x1a\x00/H\x00\x00\xeb\xad\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb4\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x00\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x00\x8a\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00^\xdca3'
eapol_sample_2 = b'\x00\x00\x1a\x00/H\x00\x00\x1c\xc0\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x00\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00w\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00I\xdaU\xb4\xc6}\x9e\xc65Z\xdb\x0e\xb5\xd1W\xf1\x15\xac\xa7qpX\xd8r\xd9\xb4=[\xf9^\xfc\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\xbd[\x89}P\x94k\xb3\xe3v#\tB\x03\xb5\x00\x18\xdd\x16\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\xaf\xab\x91\xf5'
eapol_sample_3 = b'\x00\x00\x1a\x00/H\x00\x00!\xc9\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb6\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x10\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00y\xfe\x01\xca\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x92\x9bm\x1e@`\xd2#\xbd\x91\xf6bSm\xc9\x00\x1a\xdd\x18\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\x0c\x00\x145[q'
eapol_sample_4 = b'\x00\x00\x1a\x00/H\x00\x00|\xf7\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x10\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\xb4$ocX\x84H\x99\xff\xe2\t\x11raU\x00\x00J/\xeco'

eapol_key_1 = b'\xac\x57\xc4\x5a\xb6\xa9\xc0\x7b\x0e\x03\xbb\x21\x38\xd7\x36\x89\x07\x23\x86\x30\xcb\xaa\x83\xcf\x87\x12\x72\x3d\x7f\x9a\xe3\x5f'
eapol_key_2 = b'\x49\xda\x55\xb4\xc6\x7d\x9e\xc6\x35\x5a\xdb\x0e\xb5\xd1\x57\xf1\x15\xac\xa7\x71\x70\x58\xd8\x72\xd9\xb4\x3d\x5b\xf9\x5e\xfc\x8e'

MIC_1 = b'\xdd\xbd\x5b\x89\x7d\x50\x94\x6b\xb3\xe3\x76\x23\x09\x42\x03\xb5'
MIC_2 = b'\x18\x92\x9b\x6d\x1e\x40\x60\xd2\x23\xbd\x91\xf6\x62\x53\x6d\xc9'
MIC_3 = b'\xc6\xb4\x24\x6f\x63\x58\x84\x48\x99\xff\xe2\x09\x11\x72\x61\x55'


eapol_count = 200

thread_count = 20 # !!!!!! NOT <1

except_mac = []

pkt_thread = []

packet_buffer = {}

for i in range(0,thread_count):
	pkt_thread.append(False)

def deauth(target_mac,ap_mac):
	pkt = RadioTap()/Dot11(addr1=ap_mac, addr2=target_mac, addr3=ap_mac)/Dot11Deauth(reason=7)
	rand = random.randint(0,100)
	time.sleep(rand*0.01)
	sendp(pkt,verbose=False)


def modify_mac(pkt,arg1,arg2,arg3):
	pkt = RadioTap(pkt)
	pkt[Dot11].addr1 = arg1
	pkt[Dot11].addr2 = arg2
	pkt[Dot11].addr3 = arg3

	return bytes(pkt)


def modify_key(pkt,a,arg):
	arg_num = 0
	for i in range(a,a+len(arg)):
		pkt = pkt[0:i] + arg[arg_num:arg_num+1] + pkt[i+1:len(pkt)]
		arg_num = arg_num + 1
	
	return bytes(pkt)
		


def gen_key(n):
	result = b''

	for i in range(0,n):
		random_key = random.randint(0,16*16-1)
		random_key = format(random_key,'x')
		if len(random_key) == 1:
			random_key = '0' + random_key
		result = result + bytes.fromhex(random_key)

	return result


def gen_pkt(eapol,ap_mac,target_mac):

	random_key_1 = gen_key(32)S
	random_key_2 = gen_key(32)

	random_mic_1 = gen_key(16)
	random_mic_2 = gen_key(16)
	random_mic_3 = gen_key(16)

	random_fcs_1 = gen_key(4)
	random_fcs_2 = gen_key(4)
	random_fcs_3 = gen_key(4)
	random_fcs_4 = gen_key(4)

	eapol_1 = eapol[0]
	eapol_2 = eapol[1]
	eapol_3 = eapol[2]
	eapol_4 = eapol[3]

	check_fcs = RadioTap(eapol_1).haslayer(Dot11FCS)
	if check_fcs == True:
		lower_layer = len(eapol_1) - len(bytes(RadioTap(eapol_1)[EAPOL])) - 4
	else:
		lower_layer = len(eapol_1) - len(bytes(RadioTap(eapol_1)[EAPOL]))

	eapol_1 = modify_mac(eapol_1,target_mac,ap_mac,ap_mac)
	eapol_1 = modify_key(eapol_1,lower_layer + 17,random_key_1)
	if check_fcs == True:
		eapol_1 = eapol_1 + random_fcs_1

	eapol_2 = modify_mac(eapol_2,ap_mac,target_mac,ap_mac)
	eapol_2 = modify_key(eapol_2,lower_layer + 17,random_key_2)
	eapol_2 = modify_key(eapol_2,lower_layer + 81,random_mic_1)
	if check_fcs == True:
		eapol_2 = eapol_2 + random_fcs_2

	eapol_3 = modify_mac(eapol_3,target_mac,ap_mac,ap_mac)
	eapol_3 = modify_key(eapol_3,lower_layer + 17,random_key_1)
	eapol_3 = modify_key(eapol_3,lower_layer + 81,random_mic_2)
	if check_fcs == True:
		eapol_3 = eapol_3 + random_fcs_3

	eapol_4 = modify_mac(eapol_4,ap_mac,target_mac,ap_mac)
	eapol_4 = modify_key(eapol_4,lower_layer + 81,random_mic_3)
	if check_fcs == True:
		eapol_4 = eapol_4 + random_fcs_4

	return [eapol_1,eapol_2,eapol_3,eapol_4]


def check_eap_num(pkt):
	pkt = bytes(pkt)
	check_fcs = RadioTap(pkt).haslayer(Dot11FCS)
	if check_fcs == True:
		lower_layer = len(bytes(pkt)) - len(bytes(RadioTap(pkt)[EAPOL])) - 4
	else:
		lower_layer = len(bytes(pkt)) - len(bytes(RadioTap(pkt)[EAPOL])) 
	pkt = bytes(pkt)
	eap_type = format(pkt[lower_layer + 6],'x')
	eap_nonce = format(pkt[lower_layer + 17],'x')
	if eap_type == '8a':
		return 1
	elif eap_type == 'ca':
		return 3
	elif eap_type == 'a':
		if eap_nonce == '0':
			return 4
		else:
			return 2
	else:
		return 0

send_pkt_count = 0


def eapol_jamming(eapol,replay,num,ap_mac,target_mac):
	global send_pkt_count

	for i in range(0,replay):
		pkt = gen_pkt(eapol,ap_mac,target_mac)
		for X in pkt:
			sendp(X,verbose=False)
			send_pkt_count = send_pkt_count +1
		print(send_pkt_count)
		

def thread_eapol_jamming(eapol,ap_mac,target_mac):
	tm_per = eapol_count // thread_count
	tm_extra = eapol_count % thread_count

	multi_thread_eapol_jamming = []

	deauth(target_mac,ap_mac)
	time.sleep(1)	

	for i in range(0,thread_count):
		replay = tm_per
		if i < tm_extra:
			replay = replay + 1
		multi_thread_eapol_jamming.append(threading.Thread(target=eapol_jamming, args=(eapol,replay,i,ap_mac,target_mac)))
		multi_thread_eapol_jamming[i].daemon = True
		multi_thread_eapol_jamming[i].start()

	for i in range(0,thread_count):
		multi_thread_eapol_jamming[i].join()
		print(f'No. {i} thread quit')


thread_handler = []
online_thread_num = []
online_thread_last_num = -1


def multi_thread_handler(thread_num,ap_mac,target_mac):
	global except_mac, online_thread_num, pkt_buffer, GLOBAL_INDICATE

	GLOBAL_INDICATE['sniff_protector'][0] = [target_mac,ap_mac]

	eapol = [False,False,False,False]
	
	time.sleep(1)

	for pkt in packet_buffer[f'{ap_mac}/{target_mac}']:
		eap_num = check_eap_num(pkt)-1
		eapol[eap_num] = pkt

	for i in range(0,4):
		if not eapol[i]:
			eapol[i] = eval(f'eapol_sample_{i+1}')

	thread_eapol_jamming(eapol,ap_mac,target_mac)


	time.sleep(10)

	online_thread_num.remove(thread_num)
	except_mac.remove(f'{ap_mac}/{target_mac}')
	del packet_buffer[f'{ap_mac}/{target_mac}']

	global GLOBAL_GUI
	GLOBAL_INDICATE['sniff_protector'][1] = target_mac

	print(f'finish: {ap_mac}/{target_mac}')


def handler(pkt):
	print(1)
	Dot11_len = len(bytes(pkt[Dot11]))
	Radio_len = len(bytes(pkt))

	if Radio_len - Dot11_len >= 16:

		global except_mac, online_thread_last_num, online_thread_num,thread_handler
		
		eap_num = check_eap_num(pkt)
		
		if eap_num == 1 or eap_num == 3:
			ap_mac = pkt[Dot11].addr2
			target_mac = pkt[Dot11].addr1
		elif eap_num == 2 or eap_num == 4:
			ap_mac = pkt[Dot11].addr1
			target_mac = pkt[Dot11].addr2
		else:
			ap_mac = 'X'
			target_mac = 'X'

		if not ap_mac == 'X':
			if not f'{ap_mac}/{target_mac}' in except_mac:

				print(f'start: {ap_mac}/{target_mac}')
				except_mac.append(f'{ap_mac}/{target_mac}')
				packet_buffer[f'{ap_mac}/{target_mac}'] = [bytes(pkt)]
				
				thread_num = 0
				while(True):
					if not thread_num in online_thread_num:
						break
					else:
						thread_num = thread_num + 1

				if thread_num > online_thread_last_num:
					online_thread_last_num = thread_num

					thread_handler.append(threading.Thread(target=multi_thread_handler, args=(thread_num,ap_mac,target_mac)))
				else:
					thread_handler[thread_num] = threading.Thread(target=multi_thread_handler, args=(thread_num,ap_mac,target_mac))
			
				online_thread_num.append(thread_num)
				thread_handler[thread_num].daemon = False
				thread_handler[thread_num].start()S

			packet_buffer[f'{ap_mac}/{target_mac}'].append(bytes(pkt))


def search_connection():
	while(True):
		while(GLOBAL_WIRELESS_PROTECTOR == True and status_monitor == True):
			try:
				sniff(prn=handler, filter='ether proto 0x888e', timeout=1, monitor=True, iface=GLOBAL_IFACE)
			except:
				pass
		time.sleep(1)


def start_wireless_protecter():
	thread_search = threading.Thread(target=search_connection)
	thread_search.daemon = True
	thread_search.start()
	thread_search.join()
	

#======================================================================================


def check_su():
    if os.getuid() == 0:
        return True
    else:
        return False


super_user = check_su()



def set_mode(intface,mode,gui):
	error_massege = ['Error','error','Failed','failed','not','Not']
	s_result = ''
	try:
		if mode == 0:
			gui.console.append(f'[*] InterFace: {intface} down')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} down').read()
			gui.console.append(f'[*] InterFace: Set {intface} Managed mode')
			s_result = s_result + ' ' + os.popen(f'iwconfig {intface} mode managed').read()
			gui.console.append(f'[*] InterFace: {intface} up')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} up').read()
			if s_result in error_massege:
				return False
			gui.console.append(f'[*] InterFace: Successfully Change Mode')
			return True
		elif mode == 1:
			gui.console.append(f'[*] InterFace: {intface} down')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} down').read()
			gui.console.append(f'[*] InterFace: Set {intface} Monitor mode')
			s_result = s_result + ' ' + os.popen(f'iwconfig {intface} mode monitor').read()
			gui.console.append(f'[*] InterFace: {intface} up')
			s_result = s_result + ' ' + os.popen(f'ifconfig {intface} up').read()
			if s_result in error_massege:
				return False
			gui.console.append(f'[*] InterFace: Successfully Change Mode')
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
		self.background.setPixmap(QtGui.QPixmap("GUI/GUI.png"))
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
		self.button_BF.setGeometry(QtCore.QRect(519, 510, 40, 20))
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
		self.line_monitor = QtWidgets.QTextEdit(self.centralwidget)
		self.line_monitor.setGeometry(QtCore.QRect(40, 120, 201, 31))
		self.line_monitor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_monitor.setObjectName("line_monitor")
		self.line_adaptor = QtWidgets.QTextEdit(self.centralwidget)
		self.line_adaptor.setGeometry(QtCore.QRect(40, 300, 201, 31))
		self.line_adaptor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_adaptor.setObjectName("line_adaptor")
		self.line_password = QtWidgets.QTextEdit(self.centralwidget)
		self.line_password.setGeometry(QtCore.QRect(40, 370, 201, 31))
		self.line_password.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_password.setObjectName("line_password")
		self.line_eapol = QtWidgets.QTextEdit(self.centralwidget)
		self.line_eapol.setGeometry(QtCore.QRect(450, 150, 40, 20))
		self.line_eapol.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_eapol.setObjectName("line_eapol")
		self.line_thread = QtWidgets.QTextEdit(self.centralwidget)
		self.line_thread.setGeometry(QtCore.QRect(450, 180, 40, 20))
		self.line_thread.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_thread.setObjectName("line_thread")
		self.console = QtWidgets.QTextEdit(self.centralwidget)
		self.console.setGeometry(QtCore.QRect(860, 75, 380, 610))
		self.console.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
								   "font: 12pt \"Agency FB\";\n"
								   "color: rgb(255, 255, 255);")
		self.console.setReadOnly(True)
		self.console.setObjectName("console")
		self.console_wifi = QtWidgets.QTextEdit(self.centralwidget)
		self.console_wifi.setGeometry(QtCore.QRect(20, 500, 220, 150))
		self.console_wifi.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
										"font: 12pt \"Agency FB\";\n"
										"color: rgb(255, 255, 255);")
		self.console_wifi.setReadOnly(True)
		self.console_wifi.setObjectName("console_wifi")
		self.line_channel = QtWidgets.QTextEdit(self.centralwidget)
		self.line_channel.setGeometry(QtCore.QRect(160, 440, 51, 21))
		self.line_channel.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.line_channel.setObjectName("line_channel")
		self.button_scan = QtWidgets.QPushButton(self.centralwidget)
		self.button_scan.setGeometry(QtCore.QRect(110, 465, 50, 30))
		self.button_scan.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_scan.setText("")
		self.button_scan.setIconSize(QtCore.QSize(40, 20))
		self.button_scan.setCheckable(False)
		self.button_scan.setChecked(False)
		self.button_scan.setObjectName("button_scan")
		self.button_deauth = QtWidgets.QPushButton(self.centralwidget)
		self.button_deauth.setGeometry(QtCore.QRect(498, 550, 40, 20))
		self.button_deauth.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_deauth.setText("")
		self.button_deauth.setIcon(icon)
		self.button_deauth.setIconSize(QtCore.QSize(40, 20))
		self.button_deauth.setCheckable(False)
		self.button_deauth.setChecked(False)
		self.button_deauth.setObjectName("button_deauth")
		self.button_wep = QtWidgets.QPushButton(self.centralwidget)
		self.button_wep.setGeometry(QtCore.QRect(516, 385, 40, 20))
		self.button_wep.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_wep.setText("")
		self.button_wep.setIcon(icon)
		self.button_wep.setIconSize(QtCore.QSize(40, 20))
		self.button_wep.setCheckable(False)
		self.button_wep.setChecked(False)
		self.button_wep.setObjectName("button_wep")
		self.button_wps = QtWidgets.QPushButton(self.centralwidget)
		self.button_wps.setGeometry(QtCore.QRect(516, 355, 40, 20))
		self.button_wps.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
		self.button_wps.setText("")
		self.button_wps.setIcon(icon)
		self.button_wps.setIconSize(QtCore.QSize(40, 20))
		self.button_wps.setCheckable(False)
		self.button_wps.setChecked(False)
		self.button_wps.setObjectName("button_wps")
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.line_monitor.setHtml(_translate("MainWindow",
											 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
											 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
											 "p, li { white-space: pre-wrap; }\n"
											 "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
											 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.line_adaptor.setHtml(_translate("MainWindow",
											 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
											 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
											 "p, li { white-space: pre-wrap; }\n"
											 "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
											 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.line_password.setHtml(_translate("MainWindow",
											  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
											  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
											  "p, li { white-space: pre-wrap; }\n"
											  "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
											  "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.line_eapol.setHtml(_translate("MainWindow",
										   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
										   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
										   "p, li { white-space: pre-wrap; }\n"
										   "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
										   "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.line_thread.setHtml(_translate("MainWindow",
											"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
											"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
											"p, li { white-space: pre-wrap; }\n"
											"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
											"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.console.setHtml(_translate("MainWindow",
										"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
										"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
										"p, li { white-space: pre-wrap; }\n"
										"</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
										"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.console_wifi.setHtml(_translate("MainWindow",
											 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
											 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
											 "p, li { white-space: pre-wrap; }\n"
											 "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
											 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.line_channel.setHtml(_translate("MainWindow",
											 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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

		self.button_scan.clicked.connect(self.on_scan)

		self.line_channel.textChanged.connect(self.change_channel)

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
		self.button_scan.setStyleSheet(
			'''
			QPushButton{background-color: rgba(255,255,255,0);border: 0px;}
			QPushButton:hover{background-color: rgba(39, 39, 39, 100);}
			'''
		)

		self.status_timer = QtCore.QTimer(self)
		self.status_timer.start(500)
		self.status_timer.timeout.connect(self.indicate)

	
		global GLOBAL_GUI
		GLOBAL_GUI = self

		thread_wireless_protecter = threading.Thread(target=start_wireless_protecter)
		thread_wireless_protecter.daemon = True
		thread_wireless_protecter.start()
		
		if iface.default_if() != None:
			self.line_monitor.setText(iface.default_if())
			global GLOBAL_IFACE
			GLOBAL_IFACE = iface.default_if()

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


	def indicate(self):
		global GLOBAL_INDICATE
		if GLOBAL_INDICATE['scan'] == True:
			GLOBAL_INDICATE['scan'] = False
			for x in ap_list:
				self.console_wifi.append(x)
		if not GLOBAL_INDICATE['channel_hop'] == False:
			self.console.append(f'[*] Channel hopping: {GLOBAL_INDICATE["channel_hop"]}')
			if GLOBAL_INDICATE['channel_hop'] == 11:
				self.console.append(f'[IDzone] Finish: Scanning Wi-Fi')
			GLOBAL_INDICATE['channel_hop'] = False
		if not GLOBAL_INDICATE['sniff_protector'][0] == False:
			self.console.append(f' ')
			self.console.append(f'[*] Wi-Fi Connection: {GLOBAL_INDICATE["sniff_protector"][0][0]} -> {GLOBAL_INDICATE["sniff_protector"][0][1]}')
			self.console.append(f'[*] Wireless-Sniff-Protecter PROTOCOL')
			self.console.append(f'[*] EAPOL Count: {eapol_count}')
			self.console.append(f'[*] Thread: {thread_count}')
			self.console.append(f' ')
			GLOBAL_INDICATE['sniff_protector'][0] = False
		if not GLOBAL_INDICATE['sniff_protector'][1] == False:
			self.console.append(f' ')
			self.console.append(f'[*] Wireless-Sniff-Protecter PROTOCOL')
			self.console.append(f'[*] Finish: {GLOBAL_INDICATE["sniff_protector"][1]}')
			self.console.append(f' ')
			GLOBAL_INDICATE['sniff_protector'][1] = False


	def minimize(self):
		self.showMinimized()

	def exit(self):
		sys.exit(app.exec_())



	def center(self):
		try:
			qr = self.frameGeometry()
			cp = QtCore.QDesktopWidget().availableGeometry().center()
			qr.moveCenter(cp)
			self.move(qr.topLeft())
		except:
				pass

	def mousePressEvent(self, event):
		try:
			self.oldPos = event.globalPos()
		except:
			pass

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except:
				pass


	def on_monitor(self):
		if super_user:
			global status_monitor
			adapter_name = self.line_monitor.toPlainText()
			if iface.check_if(adapter_name):
				conf.iface = adapter_name
				global GLOBAL_IFACE
				GLOBAL_IFACE = adapter_name
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


	def on_scan(self):
		scan_thread = threading.Thread(target=start_scan, args=(self,))
		scan_thread.daemon = True
		scan_thread.start()
		self.console.append(f'[IDzone] Scanning Wi-Fi...')

	
	def change_channel(self):
		allow_channel = []
		for i in range(1,13):
			allow_channel.append(str(i))
		channel_index = self.line_channel.toPlainText()
		if channel_index in allow_channel:
			os.system(f'sudo iwconfig {GLOBAL_IFACE} channel {channel_index}')
			self.console.append(f'[*] Channel is changed: {channel_index}')
		
		
	


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	myWindow = MyWindow()
	myWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	myWindow.show()
	sys.exit(app.exec_())
	MainWindow.show()
	sys.exit(app.exec_())
