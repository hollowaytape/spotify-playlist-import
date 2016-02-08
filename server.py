from flask import Flask
import os
import spotipy
import spotipy.util as util

scope = 'user-library-read'
# Eventually, I want 'playlist-modify-public'

client_id = os.environ['clientID']
client_secret = os.environ['clientSecret']
spotify_email = os.environ['spotifyEmail']
spotify_redirect_uri = os.environ['spotifyRedirectUri']

app = Flask(__name__)

@app.route("/")
def auth():
	page = ''
	token = util.prompt_for_user_token(spotify_email, scope)
	if token:
		sp = spotipy.Spotify(auth=token)
		results = sp.current_user_saved_tracks()
		for item in results['items']:
			track = item['track']
			page += track['name'] + ' - ' + track['artists'][0]['name'] + "\n"
		return page
	else:
		return "Can't get token for", spotify_email


#@app.route("/auth", methods=['GET', 'POST'])
#def login():
#	if request.method == 'POST':
#		login()

if __name__ == "__main__":
	app.run()