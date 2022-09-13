import sounddevice
import soundfile
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod, oscbuildparse

import threading
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

class OSCserver:

	def __init__(self, n, a, c):
		print("Initialising a new OSCserver")
		osc_startup()
		self.name = n
		self.address = a
		self.port = c
		self.clock = 0
		self.proc_count = 0
		self.sleeping = False
		osc_udp_server(self.address, self.port, self.name)
		osc_method(f"/{self.name}/play/*", self.receiver)
		osc_method(f"/{self.name}/terminate/*", self.bedtime)
		print(f"{self.name} live!")

	def process(self):
		print(f"{self.name} is listening... ({self.proc_count})")
		self.proc_count = self.proc_count + 1
		osc_process()

	def receiver(self, x):
		print(f"received {x} @ /play/*")
		sound = threading.Thread(target=play, args=(x,))
		sound.start()

	def tick(self):
		self.clock = (self.clock + 1) % 100000
		return True if self.clock == 0 else False

	def bedtime(self, z):
		print(f"Terminate Execution Command Received!")
		self.sleeping = True

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
	#Init a Runtime Check
	execute = True
	while execute:
		#Normal Exe
		if myOscServer.tick():
			myOscServer.process()
			execute = False if myOscServer.sleeping else True
		#Optional Safety
		if perf_counter() > 10:
			execute = False
		
	myOscServer.terminate()
	exit()