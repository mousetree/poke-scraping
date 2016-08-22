import requests
from time import sleep

base = 'https://www.pokeradar.io/api/v1/submissions?deviceId=81864d605fe911e69b3f456a8ce81a69&minLatitude=30.751277776257812&maxLatitude=47.931066347509784&minLongitude=-127.96875&maxLongitude=-69.169921875&pokemonId={}'

seen = set()
pokedex = {
	122: 'Mr. Mime',
	143: 'Snorlax',
	149: 'Dragonite',
	131: 'Lapras',
	115: 'Kangaskhan'
}


def update_map(lat, lon):
	print 'Auto-updating map....'
	sleep(10)
	update_url = 'http://127.0.0.1:5000/next_loc?lat={}&lon={}'.format(lat,lon)
	r = requests.post(update_url)
	if r.status_code == requests.codes.ok:
		print 'Success!'
	else:
		print 'Failure!'

def get (id):
	url = base.format(id)
	print 'Requesting {}: {} ....'.format(id, pokedex[id])
	try:
		r = requests.get(url)
		result = r.json()
		pokemon = result['data']
		for p in pokemon:
			trainer = p['trainerName']
			upvotes = p['upvotes']
			downvotes = p['downvotes']
			if (trainer == '(Poke Radar Prediction)') or (upvotes > 2 and downvotes == 0):
				print "\n{}: {} up, {} down".format(trainer, upvotes, downvotes)
				lat = p['latitude']
				lon = p['longitude']
				pid = str(lat)+str(lon)
				if pid not in seen:
					seen.add(pid)
					print "{},{}".format(p['latitude'],p['longitude'])
					update_map(lat,lon)
	except requests.exceptions.ConnectionError:
		print 'Could not connect.'
	print '-----\n'

while True:
	get(131)
	get(149)
	get(143)
	get(115)
	sleep(10)
