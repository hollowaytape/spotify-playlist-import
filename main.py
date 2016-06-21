from m3u import Track
import os
import json
import requests

# Grab spotify app keys.
#client_id = os.environ['clientID']
#client_secret = os.environ['clientSecret']
response_uri = 'http://localhost:8000/auth'

#playlist_file = 'test.m3u'
playlist_file = 'longer_test.m3u'
fo = open(playlist_file, 'r')
song_locs = fo.readlines()


tracks = [Track(loc) for loc in song_locs]
ids = [track.get_id() for track in tracks]

print ids
#queries = 

print tracks
#print queries

#authorize_url = "https://accounts.spotify.com/authorize/"
#authorize_query = authorize_url + "?client_id=%s&response_type=code&response_uri=%s" % (client_id, response_uri)

#authorize = requests.get(authorize_query)
#print authorize