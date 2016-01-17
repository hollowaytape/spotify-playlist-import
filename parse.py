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


#audio_formats = [".mp3", ".flac", ".m4a", ]
# This can be better accomplished by splitting at the last period.

# garbage: all the strings that appear at the beginning or end of music folders.
# The list will expand as I find more garbage.
garbage = ['v0', 'WEB V0', '[FLAC]', '320', '320kbps', 'mp3', 'CBR', 'UK',
           '(Special Edition)', '(Clean)', '(Explicit)']
garbage_years = [y for y in range(1950, 2030)]
# "But what about 1989???" Whoops, it's on Spotify now too...
garbage.extend(garbage_years)
# To remove garbage from string album_folder, split it by ' ', '-', '(', '['
# and call album_folder_parts - garbage. (Unordered shouldn't matter).

# TODO: Stuff still being identified incorrectly:
# Artist: (2014) todd terje
# Artist: 1978 # not enough info to fix; it's actually misfits
# Album: v0 # when it's locrian, and the album is 'Locrian - Return to Annihilation - 2013 - v0'
# Artist: the weeknd-beauty behind the madness-2015-h3x
# Album: the weeknd-beauty behind the madness-2015-h3x
# Track: the weeknd-cant feel my face
# Track: 4 every relationship earthrise
# Album: web v0 # when it's thundercat
# Artist: undertale soundtrack # not enough info to fix
# Album: web v0 # when it's new locrian
# Artist: mr. carmack weird bytes drugs ep (2014) [trap] # weird bytes??
# Album: pain is beauty 2013 folk 320kbs cbr mp3 # motivation for garbage list


import os

# Grab spotify app keys.
clientID = os.environ['clientID']
clientSecret = os.environ['clientSecret']

playlist_file = 'test.m3u'
fo = open(playlist_file, 'r')
song_locs = fo.readlines()

queries = []

for loc in song_locs:
	artist_in_album_folder = False
	dirs = loc.split('\\')

	artist_folder = dirs[-3]
	if artist_folder[0] == '~' or artist_folder == 'Music':
		artist_in_album_folder = True
	else:
		artist_in_album_folder = False
		artist = artist_folder.split('(')[0]
		artist = artist.split('[')[0]
		artist = artist.lower()

	album_folder = dirs[-2]
	album_folder = album_folder.replace('_', ' ')
	album_folder_parts = album_folder.split(' - ')
	print album_folder_parts
	if artist_in_album_folder:
		artist = album_folder_parts[0]

		artist = artist.lower()
	
	album = album_folder_parts[-1]
	album = album.split('(')[0]
	album = album.split('[')[0]
	# If it begins with a year, strip it and the space:
	if album[0].isdigit() and album[3].isdigit():
		album = album[5:]
	album = album.lower().strip()

	# Track filename should be the easiest one.
	track_filename = dirs[-1]
	track_filename = track_filename.replace('_', ' ')
	# Remove the track number (2 digits, 3 if grindcore) at the beginning:
	if track_filename[0].isdigit() or track_filename[0] in 'ABCD':
		track_filename = track_filename[3:]
		track_filename = track_filename.lstrip('-. ')
	
	track_filename = track_filename.rsplit('.', 1)[0]
	track = track_filename.lower()

	# TODO: This is not great yet - the really weird artist names
	# still need to be split up themselves before this works.
	# i.e. the_weeknd-beauty_behind_the_madness-2015-h3x for artist/album
	if artist in track:
		track_without_artist = track.split(artist)
		if track_without_artist[-1]:
			track = track_without_artist[-1]
			track = track.lstrip('- ')
			if track[0].isdigit() or track[0] in 'ABCD':
				track = track[3:]
				track = track.lstrip('-. ')
	# If the artist or album titles appear in the track title,
	# and removing it won't produce an empty string (example:
	# Black Sabbath - 'Black Sabbath' on Black Sabbath),
    # remove them from the track title.


	print "Artist: " + artist
	print "Album: " + album
	print "Track: " + track

	artist = artist.replace(" ", "+")
	album = album.replace(" ", "+")
	track = track.replace(" ", "+")

	if album:
		query = 'q=album:' + album + '+artist:' + artist + '+track:"' + track + '"+type:track'
		query_without_album = 'q=artist:' + artist + '+track:"' + track + '"+type:track'
		# In case the album is messed up and interferes with the search, have a backup q.
		# (But not doing anything with it yet.)
	else:
		query = 'q=artist:' + artist + '+track:"' + track + '"+type:track'
	
	#print query
	print "\n"

	queries.append(query)

print queries