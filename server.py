from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException
import os
import spotipy
import spotipy.util as util
import requests

scope = 'user-library-read'
# Eventually, I want 'playlist-modify-public'

SPOTIFY_APP_ID = os.environ['clientID']
SPOTIFY_APP_SECRET = os.environ['clientSecret']
SPOTIFY_EMAIL = os.environ['spotifyEmail']
SPOTIFY_REDIRECT_URI = os.environ['spotifyRedirectUri']

app = Flask(__name__)
app.secret_key = os.environ['flaskSecretKey']
app.debug = True
oauth = OAuth(app)

spotify = oauth.remote_app(
	'spotify',
	consumer_key=SPOTIFY_APP_ID,
	consumer_secret=SPOTIFY_APP_SECRET,
	request_token_params={'scope': scope},
	base_url="https://accounts.spotify.com/authorize/",
	request_token_url=None,
	access_token_url='/api/token',
	authorize_url='https://accounts.spotify.com/authorize'
)


@app.route("/")
def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return spotify.authorize(callback=callback)

@app.route('/login/authorized')
def spotify_authorized():
	resp = spotify.authorized_response()
	if resp is None:
		return "Access denied: reason={0} error={1}".format(
			request.args['error_reason'],
			request.args['error_description']
			)
	if isinstance(resp, OAuthException):
		return 'Access denied: {0}'.format(resp.message)

	session['oauth_token'] = (resp['access_token'], '')
	me = spotify.get('/me')
	return 'Logged in as id={0| name={1] redirect={2}'.format(
		me.data['id'],
		me.data['name'],
		request.args.get('next')
	)

@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')

if __name__ == "__main__":
	app.run()