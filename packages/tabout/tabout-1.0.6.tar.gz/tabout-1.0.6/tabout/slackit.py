import slack

def slackit(token, channel_id, script_name=False):
	client = slack.WebClient(token)
	if script_name:
		msg = "Your {} script has finished!".format(script_name)
	else:
		msg = "Your script has finished!"
	response = client.chat_postMessage(channel=channel_id, text=msg, username='Tabout Bot')