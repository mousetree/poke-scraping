import requests
import datetime as dt
import time
import os
import random
from termcolor import colored, cprint

URL = 'https://skiplagged.com/api/pokemon.php?bounds=40.750899,-74.030798,40.803091,-73.907202'
TARGETS = [
	'snorlax',
	'dratini',
	'dragonair'
	'dragonite',
	'lapras',
	'blastoise',
	'charizard',
	'omanyte',
	'omastar',
	'chansey',
	'hitmonlee',
	'kabuto',
	'kabutops',
	'aerodactyl',
	'muk',
	'charmander',
	'charmeleon'
]
INTERVAL = 30 # seconds
SEEN = set()
VOICES = None

def get_pokemon():
	print "Requesting Pokemon..."
	r = requests.get(URL)
	pokemon = r.json()['pokemons']
	return list(p for p in pokemon if p['pokemon_name'].lower() in TARGETS)


def print_results(pokemons):
	now = dt.datetime.now()
	for p in pokemons:
		name = p['pokemon_name']
		lat = p['latitude']
		lon = p['longitude']
		expires = dt.datetime.fromtimestamp(p['expires'])
		if expires < now:
			return
		diff = expires - now
		delta = divmod(diff.days * 86400 + diff.seconds, 60)
		pid = make_id(p)
		seen = pid in SEEN
		color = 'yellow' if seen else 'green'

		print ''
		print colored(name, color), '[{}m {}s]'.format(delta[0], delta[1])
		print colored("{},{}".format(lat,lon), 'blue')

		if not seen:
			SEEN.add(pid)
			# say(name)
			update_map(lat, lon)
			time.sleep(10)
				

def make_id(p):
	name = p['pokemon_name']
	lat = str(round(p['latitude'],3))
	lon = str(round(p['longitude'],3))
	expires = str(int(p['expires']/100))
	return name+lat+lon+expires

def say(text):
	voice = random.choice(VOICES)
	print 'Voice: {}'.format(voice)
	os.system('say -v "{}" "{}"'.format(voice, text))

def update_map(lat, lon):
	print 'Auto-updating map....'
	update_url = 'http://127.0.0.1:5000/next_loc?lat={}&lon={}'.format(lat,lon)
	r = requests.post(update_url)
	if r.status_code == requests.codes.ok:
		print 'Success!'
	else:
		print 'Failure!'

def get_voices():
	voices = []
	output = os.popen('say -v "?"').read().split('\n')
	for line in output:
		name = line.split('  ')[0]
		voices.append(name)
	return voices

def main():
	global VOICES
	VOICES = get_voices()
	while True:
		try:
			matches = get_pokemon()
			uniques = {v['pokemon_name']+str(round(v['latitude'],2)):v for v in matches}.values()
			print '{} unique matches found'.format(len(uniques))
			if len(uniques) > 0:
				print_results(uniques)
				# say('Pokemon')
			interval = random.randint(INTERVAL, INTERVAL+15)
			print '\nWaiting {}s'.format(interval)
			time.sleep(interval)
			print '\n--------\n'
		except requests.exceptions.ConnectionError:
			print 'Could not retrieve Pokemon from SkipLagged.'

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		print 'Exiting...'
