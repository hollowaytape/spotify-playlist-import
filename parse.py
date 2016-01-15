# Takes a m3u file, which is essentially a list of file paths,
# and returns a list of (Artist, Album, Track) tuples to plug into the
# Spotify API track search.

# More of a prototype, just to see if it can be done.
# This is more of a thing to do in js so you can upload files to it.

audio_formats = [".mp3", ".flac", ".m4a", ]

playlist_file = 'test.m3u'
fo = open(playlist_file, 'r')
song_locs = fo.readlines()

for loc in song_locs:
	artist_in_album_folder = False
	dirs = loc.split('\\')

	artist_folder = dirs[-3]
	# Stuff in ~receiving has the artist in the album folder name.
	# (Tried to write this concisely and got a NameError.)
	if artist_folder[0] == '~':
		artist_in_album_folder = True
	else:
		artist_in_album_folder = False
		artist = artist_folder

	album_folder = dirs[-2]
	album_folder = album_folder.replace('_', ' ')
	album_folder_parts = album_folder.split(' - ')
	print album_folder_parts
	if artist_in_album_folder:
		artist = album_folder_parts[0]
	
	album = album_folder_parts[-1]
	album = album.split('(')[0]
	album = album.split('[')[0]
	#print album

	# Track filename should be the easiest one.
	track_filename = dirs[-1]
	track_filename = track_filename.replace('_', ' ')
	# Remove the track number (2 digits) at the beginning:
	if track_filename[0].isdigit():
		# TODO: multidisc track numbers 1-02 and B2 still remain.
		track_filename = track_filename[2:]
		track_filename = track_filename.lstrip('-. ')
	
	track_filename = track_filename.rsplit('.', 1)[0]

	# TODO: This is not helpful yet - the really weird artist names
	# still need to be split up themselves before this works.
	if artist in track_filename:
		print track_filename.split(artist)


	print "Artist: " + artist
	print "Album: " + album
	print "Track: " + track_filename
	print "\n"


	# If the artist or album titles appear in the track title,
	# and removing it won't produce an empty string (example:
		# Black Sabbath - 'Black Sabbath' on Black Sabbath),
    # remove them from the track title.