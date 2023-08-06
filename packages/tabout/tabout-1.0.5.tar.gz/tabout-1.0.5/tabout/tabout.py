from .soundit import soundit
from .slackit import slackit
import os

def alertme(sound = True, token = False, channel = False, script = False):

	cwd = (os.path.dirname(__file__))
	sound_file = cwd + '/sounds/alert1.tabout.mp3'

	if sound:
		soundit(sound_file)
	if token and channel:
		slackit(token, channel, script)
