import sounddevice
import soundfile
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod, oscbuildparse

import threading
import json
from time import perf_counter, sleep

from OSCSoundTrigger import read_config, play, OSCserver

def send(address, message):
	print(f"sending {message} -> {address}")
	msg = oscbuildparse.OSCMessage(f"/{config['server_name']}/{address}", None, [message])
	osc_send(msg, 'tester')
	myOscServer.process()

def run_a_test():
	print("Running test : you should hear a sound, then OSCSoundTriggerServer should Terminate.")
	send('play/me', 'cherokee.wav')
	send('terminate/me', None)

if __name__ == '__main__':
	#Get Configuration Settings
	config = read_config()
	#Make Server
	myOscServer = OSCserver(config['server_name'], config['network']['address'], config['network']['port'])
	#Setup Client for testing
	osc_udp_client(config['network']['address'], config['network']['port'], 'tester')
	execute = True
	run_a_test()
	while execute:
		#Normal Exe
		if myOscServer.tick():
			myOscServer.process()
			execute = False if myOscServer.sleeping else True
		#Optional Safety
		if perf_counter() > 30:
			execute = False
		
	myOscServer.terminate()
	exit()