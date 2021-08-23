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