# Takes a m3u file, which is essentially a list of file paths,
# and returns a list of (Artist, Album, Track) tuples to plug into the
# Spotify API track search.

# So, the difficulty with the m3u filetype (and the reason that others
# have released stuff that doesn't work) is that it only has filenames/paths.
# You can't search by track number on spotify, at least directly.
# So the only thing you might have for sure is the track name, which
# will most likely not return the right song.

# A few different approaches I could take here:
# 1) Desktop version. Here you can actually access the mp3 tags on the
#    user's machine, so you'd get the best results this way.
# 2) Web version. If the files are well-organized in the first place,
#    this will work well, but will be very haphazard if not.
# 3) Slow web version. Takes into account track number, looks at a bunch
#    of the results and determines which one is in the right position.

# garbage: all the strings that appear at the beginning or end of music folders.
garbage = ['v0', 'web v0', '320', '320kbps', '320kbs', 'mp3', 'cbr', 'uk',
           'special', 'edition', 'clean', 'explicit', 'h3x', 'vtwin88cube']
garbage_years = [str(y) for y in range(1950, 2030)]
# "But what about 1989???" Whoops, plus it's on Spotify now too...
garbage.extend(garbage_years)
# To remove garbage from string album_folder, split it by ' ', '-', '(', '['
# and call album_folder_parts - garbage. (Unordered shouldn't matter).

# Regex to match anything in ()s, []s, or {}s. (Covers a lot, but not all)
garbage_regex = r'[\(\{\[][^)]*[\)\}\]]'

def remove_garbage(a):
    for e in a[:]:  # Avoids deleting items from list while iterating
        if e.lower().strip() in garbage:
            a.remove(e)

import re

class Track:
	def __init__(self, loc):
		# Takes a path to a file and calculates the name, artist, and album.
		# Initialize vars
		artist = ''
		album = ''
		track = ''
		artist_in_album_folder = False

		dirs = loc.split('\\')

		# Artist name.
		artist_folder = dirs[-3]
		# Artists in a ~receiving or Music folder might have a name in the album folder.
		# Delay determination of the artist name for these special cases.
		artist_in_album_folder = (artist_folder[0] == '~' or artist_folder == 'Music')
		if not artist_in_album_folder:
			artist = re.sub(garbage_regex, '', artist_folder).lower()
			# these are being calculated just fine

		# Album name.
		album_folder = dirs[-2]
		album_folder = re.sub(garbage_regex, '', album_folder).replace('_', ' ')
		# Separate by '-' and remove whitespace of each part.
		#TODO: This still doesn't catch garbage when it's not separated with -[](){}...
		album_folder_parts = [x.strip() for x in album_folder.split('-')]
		remove_garbage(album_folder_parts)

		if artist_in_album_folder:
			album = album_folder_parts.pop().lower()
			if not album_folder_parts:    # self titled albums become empty
				album_folder_parts.append(album)
			artist = album_folder_parts[0].lower()

		else:
			album = album_folder_parts[0]
		#album = re.sub(r'\([^)]*\)', '', album)
		# If it begins with a year, strip it and the space:
		if album:
			if album[0].isdigit() and album[3].isdigit():
				album = album[5:]
			album = album.lower().strip()

		# Track name.
		track_filename = dirs[-1].replace('_', ' ')
		# Remove the track number (2 digits, 3 if grindcore) at the beginning:
		if track_filename[0].isdigit() or track_filename[0] in 'ABCD':
			track_filename = track_filename[3:].lstrip('-. ')
		track = track_filename.rsplit('.', 1)[0].lower()

		if artist in track:
			track = track.replace(artist, '')
			if track[0].isdigit() or track[0] in 'ABCD':
				track = track[3:]
			track = track.lstrip('-. ')
		# TODO: Deal with self-titled tracks.

		self.name = track
		self.artist = artist
		self.album = album


		#print "Artist: " + artist
		#print "Album: " + album
		#print "Track: " + track

		artist = artist.replace(" ", "+")
		album = album.replace(" ", "+")
		track = track.replace(" ", "+")
		
	def query(self):
		if album:
			query = 'q=album:' + album + '+artist:' + artist + '+track:"' + track + '"&type=track'
			#query_without_album = 'q=artist:' + artist + '+track:"' + track + '"&type=track'
			# In case the album is messed up and interferes with the search, have a backup q.
			# (But not doing anything with it yet.)
		else:
			query = 'q=artist:' + artist + '+track:"' + track + '"&type=track'
		return query

	def __repr__(self):
		return self.artist + " - " + self.name