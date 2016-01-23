from m3u import Track
import os
import json
import requests

# Grab spotify app keys.
clientID = os.environ['clientID']
clientSecret = os.environ['clientSecret']

playlist_file = 'test.m3u'
fo = open(playlist_file, 'r')
song_locs = fo.readlines()


tracks = [Track(loc) for loc in song_locs]
#queries = 

#print tracks
#print queries

url = 'https://api.spotify.com/v1/search?'
for query in [track.query for track in tracks]:
	resp = requests.get(url + query) # TODO: don't forget to sanitize.
	print resp
	if resp.status_code != 200:
		# This means something went wrong.
		# No such thing as an APIError
		#raise APIError('GET /serach/ {}'.format(resp.status_code))
		pass
	try:
		values = resp.json()['tracks']['items'][0]
		print values['name']
		print values['album']['name']
	except IndexError:
		print "Could not find track with query %s" % query