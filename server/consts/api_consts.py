import os

PLAYLIST_LINK_FORMAT = 'https://open.spotify.com/playlist/{}'
ID = 'id'
MAX_SPOTIFY_PLAYLIST_SIZE = os.getenv("MAX_SPOTIFY_PLAYLIST_SIZE", 25)
MAX_TRACKS_NUMBER_PER_REQUEST = 50
