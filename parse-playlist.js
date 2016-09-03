// Takes a playlist file (xspf, later m3u) and determines the Spotify IDs of each.
// Or maybe it just determines the track name and artist??
// Not sure what level of separation from the Spotify API I want here.

var fs = require('fs');
var path = require('path');
var parseString = require('xml2js').parseString;

var testFile = path.join(__dirname, 'test.xspf');

exports.getTracks = function(xspf_string, handleTracks) {
	// kept returning undefined due to an unescaped "&" in Glassjaw - Worship & Tribute...
	// TODO: Validate the xml for other things before passing it to xml2js (parseString).
	cleanXML = xspf_string.replace(/&/g, "&amp;");

	parseString(cleanXML, function(error, result) {
		if (error) throw error;
		var tracks = result.playlist.trackList[0].track;
		var parsedTracks = [];
		tracks.forEach(function(track) {
			parsedTrack = {
				title: track.title[0],
				artist: track.creator[0],
				album: track.album[0]
			};
			parsedTracks.push(parsedTrack);
		})
		handleTracks(parsedTracks);
	});
};