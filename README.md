# OSCSoundTrigger
Simple script for triggering .wav files using OSC. 

## Dependencies
- https://pypi.org/project/SoundFile/
- https://pypi.org/project/sounddevice/
- https://pypi.org/project/osc4py3/

## Getting Started

#### Edit the config.json file to a IP4 and port of your preference.
WARNING : Please put your personal configuration into a .gitignore file.
```json
{"network": {"address": "MY_ADDRESS","port": "MY_PORT"},
	"server_name": "MY_SERVER"}
```
#### Test the configurations using testbed.
```bash
python3 testbed.py
```
#### When you're comfident you can receive external messaging remove the auto exit safety.
```python
while execute:
	#Optional Safety
	if perf_counter() > 10:
		execute = False
```

## Creating a custom handler

#### Documentation
https://osc4py3.readthedocs.io/en/latest/userdoc.html

#### Example
```python
class Child_OSC_Server(OSCserver):
  def __init__(self, n, a, c):
    OSCserver.__init__(self, n, a, c)
    osc_method(f"/{self.name}/MY_HANDLER/*", self.MY_HANDLER_FUNCTION)
  def MY_HANDLER_FUNCTION(self, *args):
    # Wait for x,y,z of new location.
    #DO SOMETHING HERE WHEN /{self.name}/MY_HANDLER/* RECEIVES AN OSC MESSAGE
    pass
```

## Playing Sound

#### Finding and selcting pythons sound device
```bash
python3 -m sounddevice
```
```python
import sounddevice as sd
sd.default.samplerate = 44100
sd.default.device = 'digital output'
```

#### The Play Function
play(x) expects the absolute of relative path of a play file.
Simplest soltion is to create a folder of audio files and in your repos local directory.
WARNING: Please put any audio files into your .gitignore. Pull requests with .wav files will not be accepted.

## Contribution
MIT Licence Applies.
Issues welcome.
