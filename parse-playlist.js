// Takes a playlist file (xspf, later m3u) and determines the Spotify IDs of each.
// Or maybe it just determines the track name and artist??
// Not sure what level of separation from the Spotify API I want here.

var fs = require('fs');
var path = require('path');
var parseString = require('xml2js').parseString;

var testFile = path.join(__dirname, 'test.xspf');

var parsers = {
  '.xspf': parseXSPF,
  '.m3u': parseM3U,
  '.m3u8': parseM3U,
};

var audioFormats = ['.mp3', '.m4a', '.flac', '.wav', '.ape', '.aiff', '.pcm', 'wma'];

function cleanFilename(filename) {
  console.log(filename);
  var regex = /\d{2,3} (.*)\..{3,4}/g;
  var match = regex.exec(filename);
  var base = match[1];
  base = base.replace("-", "");
  base = base.replace(/\s+$/, '');
  return base;
}

function parseXSPF(file_string, handleTracks) {
  // xspf files are easy - they have artist and title in clearly labeled XML.

  // TODO: Use a real library for this to catch stuff other than the & in "Worship & Tribtue".
  cleanXML = file_string.replace(/&/g, "&amp;");

  parseString(cleanXML, function(error, result) {
    if (error) throw error;
    var tracks = result.playlist.trackList[0].track;
    var parsedTracks = [];
    tracks.forEach(function(track, index) {
      parsedTrack = {
        title: track.title[0],
        artist: track.creator[0],
        album: track.album[0],
        position: index
      };
      parsedTracks.push(parsedTrack);
    })
    handleTracks(parsedTracks);
  });
}

function parseM3U(file_string, handleTracks) {
  // m3u is the most difficult one. It all depends on how the files are organized in the user's system.
  // First try is to interpret it in the iTunes "Organize My Music" format, ..\Music\[artist]\[album]\[track#] [trackname][extension].
  // That's really easy. But when you have it organized even slightly differently, everything breaks.
  // Or when you have artist and album named in the same folder, along with a [320] tag or a (v0) tag or a ripper name or w/e.

  console.log(file_string);
  var tracks = file_string.split("\n");
  var parsedTracks = [];

  if (tracks[0] == "#EXTM3U") {
    console.log("It's actually extended m3u, so need to use a different parser");
    parseExtendedM3U(file_string, handleTracks);
  } else {
  tracks.forEach(function(track, index) {
    if (track != "") {
      var fields = track.split("\\");
      console.log(fields);

      var title = cleanFilename(fields[fields.length-1]);
      var artist = fields[fields.length-3]

      if (title.indexOf(artist) != -1) {
        console.log("Found the artist in the filename");
        title = title.replace(artist, '');
      }

      parsedTrack = {
        title: title,
        album: fields[fields.length-2],
        artist: artist,
        position: index,
      }
      console.log(parsedTrack);
      parsedTracks.push(parsedTrack);
    }
  });
  handleTracks(parsedTracks);
  }
}

function parseExtendedM3U(file_string, handleTracks) {
  parsedTracks = [];
  handleTracks(parsedTracks);
}

exports.getTracks = function(filetype, file_string, handleTracks) {
  var parser = parsers[filetype];
  parser(file_string, handleTracks);
};

exports.trackPositionSort = function(a, b) {
  return a.position - b.position;
};