var express = require('express'); // Express web server framework
var app = express();

// Spotify API and app information is stored in the environment variables
var client_id = process.env.CLIENT_ID;
var client_secret = process.env.CLIENT_SECRET;
var redirect_uri = process.env.SPOTIFY_REDIRECT_URI;

var SpotifyWebApi = require('spotify-web-api-node');

var spotifyApi = new SpotifyWebApi({
	clientId: client_id,
	clientSecret: client_secret,
	redirectUri: redirect_uri
});
// spotifyApi.setAccessToken('<your_access_token>');

var scopes = ['playlist-modify-public'],
    state = 'some-state-of-my-choice';

// use multer for handling file uploads
var multer = require('multer');
var upload = multer({ dest: './uploads/'});
var fs = require('fs');
var path = require('path');

var port = process.env.PORT || 8888;

//app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
	var authorizeURL = spotifyApi.createAuthorizeURL(scopes, state);
	console.log(authorizeURL);
	res.send("<a href='" + authorizeURL + "'>First, login to Spotify here</a>");

	//res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/callback', function(req, res) {
	//console.log(req);
	var authCode = req.query.code;
	spotifyApi.authorizationCodeGrant(authCode).then(function(data) {
	    // Set the access token on the API object to use it in later calls
	    spotifyApi.setAccessToken(data.body['access_token']);
	    spotifyApi.setRefreshToken(data.body['refresh_token']);

    }, function(err) {
	    console.log('Something went wrong!', err);
	    });

	res.sendfile('./index.html');
});

app.post('/callback', upload.single('playlistFile'), function(req, res, next) {
	console.log(req.file);
	if (req.file) {
		if (req.file.size === 0) {
			return next("Error: Select a file to upload first.");
		} else {
			fs.readFile(req.file.path, 'utf8', function(err, fileData) {
				if (err) return console.log(err);
				spotifyApi.getMe()
				  .then(function(userData) {
				    console.log('Some information about the authenticated user', userData.body);
				    console.log(userData.body.id, req.file.originalname);
				    spotifyApi.createPlaylist(userData.body.id, req.file.originalname, {'public': true })
				    	.then(function(playlistData) {
				    		console.log("Created playlist!");
				    		res.send(playlistData);
				    	}, function(err) {
				    		console.log("Something went wrong:", err);
				    	});

				  }, function(err) {
				    console.log('Something went wrong!', err);
				});
			});
		}
	} 

});

app.listen(port, function() {
	console.log("Express listening on " + port);
});