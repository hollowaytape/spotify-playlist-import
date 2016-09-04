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

var scopes = ['playlist-modify-public'],
    state = 'alaska';

// use multer for handling file uploads
var multer = require('multer');
var upload = multer({ dest: './uploads/'});
var fs = require('fs');
var path = require('path');

var pug = require('pug');

app.set('views', './views');
app.set('view engine', 'pug');

var parsePlaylist = require('./parse-playlist.js');

var port = process.env.PORT || 8888;

app.get('/', function(req, res) {
  if (req.query.code) {
    var authCode = req.query.code;
    spotifyApi.authorizationCodeGrant(authCode).then(function(data) {
        // Set the access token on the API object to use it in later calls
        spotifyApi.setAccessToken(data.body['access_token']);
        spotifyApi.setRefreshToken(data.body['refresh_token']);
        getUsername();
      }, function(err) {
        console.log('Something went wrong!', err);
    });

    function getUsername() {
      spotifyApi.getMe()
      .then(function(userData) {
        res.render('index', {
          loggedIn: true,
          username: userData.body.display_name
        })
      }, function(err) {
        console.log(err);
        res.render('index', {
          loggedIn: true,
          username: "you"
        })
      });
    }


  } else {
    var authorizeURL = spotifyApi.createAuthorizeURL(scopes, state);

    res.render('index', {
      loggedIn: false,
      authorizeURL: authorizeURL
    });
  }
});

app.post('/', upload.single('playlistFile'), function(req, res, next) {
  console.log(req.file);
  if (req.file) {
    if (req.file.size === 0) {
      return next("Error: Select a file to upload first.");
    } else {
      fs.readFile(req.file.path, 'utf8', function(err, fileData) {
        if (err) throw err;
        // xspf only for now!!
        parsePlaylist.getTracks(fileData, function handleTracks(tracks) {
          //console.log(tracks);
          var trackIds = [];
          var tracksQueried = 0;
          tracks.forEach(function(track, index, array) {
            // need a callback when this forEach is complete...
            var query = "track:" + track.title + " artist:" + track.artist;

            spotifyApi.searchTracks(query)
              .then(function(data) {
                tracksQueried++;
                var spotifyTrack = data.body.tracks.items[0];
                //console.log(spotifyTrack.name);
                track.spotifyUri = spotifyTrack.uri;
                
                //console.log(tracksQueried, array.length);
                if (tracksQueried === array.length) {
                  var sortedTracks = tracks.sort(parsePlaylist.trackPositionSort);
                  createPlaylist(sortedTracks);
                }
              }, function(err) {
                tracksQueried++;
                console.log('Something went wrong!', err);
                
                console.log(tracksQueried, array.length);
                if (tracksQueried === array.length) {
                  var sortedTracks = tracks.sort(parsePlaylist.trackPositionSort);
                  createPlaylist(sortedTracks);
                }
              })
          });
        });

        function createPlaylist(tracks) {
          spotifyApi.getMe()
            .then(function(userData) {
              console.log('Some information about the authenticated user', userData.body);
              var userId = userData.body.id;
              var playlistName = req.file.originalname; // TODO: Remove extension

              spotifyApi.createPlaylist(userId, playlistName, {'public': true })
                .then(function(playlistData) {
                  console.log("Created playlist!");
                  populatePlaylist(playlistData, tracks);
                }, function(err) {
                  console.log("Something went wrong:", err);
                });

            }, function(err) {
              console.log('Something went wrong!', err);
          });
        };

        function populatePlaylist(playlist, tracks) {
          console.log("populatePlaylist got called");
          //console.log(playlist);
          console.log(playlist); // check this to find the userId
          var userId = playlist.body.owner.id;
          var playlistId = playlist.body.id;
          var trackUris = tracks.map(function(track) { return track.spotifyUri });
          var trackUrisCleaned = trackUris.filter(function(uri) { return uri !== undefined });

          console.log("userId:", userId);
          console.log("playlistId", playlistId);
          console.log(trackUrisCleaned);
          spotifyApi.addTracksToPlaylist(userId, playlistId, trackUrisCleaned)
            .then(function(populatedPlaylistData) {
              console.log("Populated playlist!");
              console.log(populatedPlaylistData);
              res.send("Playlist populated! Login to spotify and look for the playlist", playlist.body.name, ".");
            }, function(err) {
              console.log("Something went wrong...", err);
            });
        };
      });
    }
  } 
});

app.listen(port, function() {
  console.log("Express listening on " + port);
});