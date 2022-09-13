import sounddevice
import soundfile
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod, oscbuildparse

import json
from time import perf_counter, sleep

def read_config():
	with open('config.json', 'r') as f:
  		return json.load(f)

def play(w):
	'''Play a Wave File.
	args :
		w -> String : Valid path for an audio wave file.
	returns : 
		The status of the SoundDevice.'''
	d, f = soundfile.read(w, dtype='float32')  
	sounddevice.play(d, f)
	return sounddevice.wait()

def send(address, message):
	print(f"sending {message} -> {address}")
	msg = oscbuildparse.OSCMessage(f"/{config['server_name']}/{address}", None, [message])
	osc_send(msg, 'tester')
	myOscServer.process()

def run_a_test():
	print("Running test : you should hear a sound, then OSCSoundTriggerServer should Terminate.")
	send('play/me', 'cherokee.wav')
	send('terminate/me', None)

class OSCserver:

	def __init__(self, n, a, c):
		print("Initialising a new OSCserver")
		osc_startup()
		self.name = n
		self.address = a
		self.port = c
		self.clock = 0
		self.proc_count = 0
		osc_udp_server(self.address, self.port, self.name)
		osc_method(f"/{self.name}/play/*", self.receiver)
		osc_method(f"/{self.name}/terminate/*", self.bedtime)
		print(f"{self.name} live!")

	def process(self):
		print(f"{self.name} is listening... ({self.proc_count})")
		osc_process()

	def receiver(self, x):
		print(f"received {x} @ /play/*")
		play(x)

	def tick(self):
		self.clock = (self.clock + 1) % 100000
		self.proc_count += 1
		return True if self.clock == 0 else False

	def bedtime(self, z):
		print(f"Terminate Execution Command Received!")
		execute = False
		print(f"execute = {execute}")

	def terminate(self):
		print(f"Goodbye {self.name} <3.")
		osc_terminate()

	def __del__(self):
		osc_terminate()

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
		#Optional Safety
		if perf_counter() > 30:
			execute = False
		
	myOscServer.terminate()
	exit()