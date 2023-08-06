import json
import os

config = os.path.dirname(__file__) + '/config.json'


def get(key):
	global config
	if not os.path.isfile(config):
		return ''
	with open(config, 'r') as f:
		data = json.load(f)
		if key in data:
			return data[key]
		f.close()


def set(key, val):
	global config

	if not os.path.isfile(config):
		with open(config, 'a') as f:
			f.write('{}')
			f.close()

	with open(config, 'r+') as f:
		data = json.load(f)
		data[key] = val
		f.seek(0)
		json.dump(data, f, indent=4)
		f.truncate()
		f.close()
