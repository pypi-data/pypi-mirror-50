from .soundit import soundit
from .slackit import slackit
from pox.shutils import find

def alertme(sound = True, token = False, channel = False, script = False):
	sound_file = find('alert1.tabout.mp3')[0]

	if sound:
		soundit(sound_file)
	if token and channel:
		slackit(token, channel, script)
