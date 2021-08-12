from scapy.all import *
import random

#iso-8859-1

target_mac = 'f0:8a:76:fd:12:42'
gateway_mac = '70:5d:cc:f1:33:ad'

conf.iface = "wlan0"

def random_nonce():
	result = b''
	for i in range(1,33):
		rand_byte = format(random.randint(0,16*16),x)

def pkttobyte(pkt):
	result_pkt = ''

	pkt = str(pkt)[2:len(str(pkt))-1]
	pkt = pkt.split('\\x')

	for i in range(1,len(pkt)):
		x = pkt[i]
		if len(x) != 2:
			x1 = x[0:2]
			x2 = x[2:len(x)]
			result_pkt = result_pkt + '=' + x1
			for x3 in x2:
				result_pkt = result_pkt + '=' + x3.encode('iso-8859-1').hex()
		else:
			result_pkt = result_pkt + '=' + x
		
	return result_pkt

def eap_sniff(pkt):
	pkt[Dot11].addr1 = gateway_mac
	pkt[Dot11].addr2 = gateway_mac
	pkt[Dot11].addr3 = target_mac
	print(pkttobyte(pkt))
	print('====================')
#	sendp(pkt, monitor=True)

sniff(offline='eap.pcapng', prn=eap_sniff)
