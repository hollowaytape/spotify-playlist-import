from m3u import Track
import os
import json
import requests

# Grab spotify app keys.
client_id = os.environ['clientID']
client_secret = os.environ['clientSecret']
response_uri = 'http://localhost:8000/auth'

playlist_file = 'test.m3u'
fo = open(playlist_file, 'r')
song_locs = fo.readlines()


tracks = [Track(loc) for loc in song_locs]
ids = [track.get_id() for track in tracks]

print ids
#queries = 

#print tracks
#print queries


#for query in [track.query for track in tracks]:
#	resp = requests.get(url + query) # TODO: don't forget to sanitize.
#	print resp
#	if resp.status_code != 200:
		# This means something went wrong.
		# No such thing as an APIError
		#raise APIError('GET /serach/ {}'.format(resp.status_code))
#		pass
#	try:
#		values = resp.json()['tracks']['items'][0]
#		print values['name']
#		print values['album']['name']
#
#	except IndexError:
#		print "Could not find track with query %s" % query

authorize_url = "https://accounts.spotify.com/authorize/"
authorize_query = authorize_url + "?client_id=%s&response_type=code&response_uri=%s" % (client_id, response_uri)

authorize = requests.get(authorize_query)
print authorize.json()