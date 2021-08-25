from scapy.all import *
import os


def default_if():
	if_list = get_if_list()
	for x in if_list:
		if 'w' in x:
			return x
	return None


def check_monitor(iface):
	word_list = ['Mode:Monitor','Monitor','monitor','mode:monitor']
	result = os.popen(f'iwconfig {iface}').readlines()
	for x in result:
		for w in word_list:
			if w in x:
				return True
	return False

def check_if(intface):
	if_list = get_if_list()
	if intface == '' or not intface in if_list:
		return False
	else:
		return True