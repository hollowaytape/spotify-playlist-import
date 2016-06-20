"""XSPF parser for the Spotify playlist converter."""

# Looks like xspf might be a file that gets much more accurate results than m3u,
# since it stores actual media tags in an XML format rather than depending on the user's dir structure.

# Plus all the services that do this are currently down for reconstruction after Spotify changed the API...
# Sounds like a good time to do some work on this!

import xml.etree.ElementTree as ET

# One progress step might be: Read the title from the xspf file, create a new spotify playlist with that name.
