#from scapy.all import *
import random

eapol_1 = b'\x00\x00\x1a\x00/H\x00\x00\xeb\xad\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb4\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x00\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x00\x8a\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00^\xdca3'
eapol_2 = b'\x00\x00\x1a\x00/H\x00\x00\x1c\xc0\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x00\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00w\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00I\xdaU\xb4\xc6}\x9e\xc65Z\xdb\x0e\xb5\xd1W\xf1\x15\xac\xa7qpX\xd8r\xd9\xb4=[\xf9^\xfc\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\xbd[\x89}P\x94k\xb3\xe3v#\tB\x03\xb5\x00\x18\xdd\x16\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\xaf\xab\x91\xf5'
eapol_3 = b'\x00\x00\x1a\x00/H\x00\x00!\xc9\x91\xaa\x00\x00\x00\x00\x10\x02\x8f\t\xa0\x00\xb6\x00\x00\x00\x88\x02:\x01\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\xbc\x96\x80\xb4aQ\x10\x00\x00\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00y\xfe\x01\xca\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\xacW\xc4Z\xb6\xa9\xc0{\x0e\x03\xbb!8\xd76\x89\x07#\x860\xcb\xaa\x83\xcf\x87\x12r=\x7f\x9a\xe3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x92\x9bm\x1e@`\xd2#\xbd\x91\xf6bSm\xc9\x00\x1a\xdd\x18\x00P\xf2\x01\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x04\x01\x00\x00P\xf2\x02\x0c\x00\x145[q'
eapol_4 = b'\x00\x00\x1a\x00/H\x00\x00|\xf7\x91\xaa\x00\x00\x00\x00\x10\x16\x8f\t\xa0\x00\xd8\x00\x00\x00\x88\x01\x02\x01\xbc\x96\x80\xb4aQ\xf0\x8av\xfd\x12B\xbc\x96\x80\xb4aQ\x10\x00\x06\x00\xaa\xaa\x03\x00\x00\x00\x88\x8e\x01\x03\x00_\xfe\x01\n\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\xb4$ocX\x84H\x99\xff\xe2\t\x11raU\x00\x00J/\xeco'

eapol_key_1 = '=ac=57=c4=5a=b6=a9=c0=7b=0e=03=bb=21=38=d7=36=89=07=23=86=30=cb=aa=83=cf=87=12=72=3d=7f=9a=e3=5f'
eapol_key_2 = '=49=da=55=b4=c6=7d=9e=c6=35=5a=db=0e=b5=d1=57=f1=15=ac=a7=71=70=58=d8=72=d9=b4=3d=5b=f9=5e=fc=8e'

MIC_1 = '=dd=bd=5b=89=7d=50=94=6b=b3=e3=76=23=09=42=03=b5'

#iso-8859-1

target_mac = 'f0:8a:76:fd:12:42'
gateway_mac = '70:5d:cc:f1:33:ad'

#conf.iface = "wlan0"

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

def gen_key(n):
    result = ''
    for i in range(0,n):
        random_key = random.randint(0,16*16)
        random_key = format(random_key,'x')
        if len(random_key) == 1:
            random_key = '0'+ random_key
        result = result + '=' + random_key
    return random_key
        

def modify_handshaking():
	#pkt[Dot11].addr1 = gateway_mac
	#pkt[Dot11].addr2 = gateway_mac
	#pkt[Dot11].addr3 = target_mac
    
        random_key_1 = gen_key(32)
        random_key_2 = gen_key(32)

        random_mic_1 = gen_key(16)
        
        pkt_1 = pkttobyte(eapol_1)
        pkt_1 = pkt_1.replace(eapol_key_1,random_key_1)
        print(pkt_1)
        print('=============')

        pkt_2 = pkttobyte(eapol_2)
        pkt_2 = pkt_2.replace(eapol_key_2,random_key_1)
        print(pkt_2)
        
#	sendp(pkt, monitor=True)

modify_handshaking()
