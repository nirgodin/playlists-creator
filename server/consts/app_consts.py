import os

PLAYLIST_DETAILS = 'playlistDetails'
ACCESS_CODE = 'accessCode'
IS_SUCCESS = 'isSuccess'
MESSAGE = 'message'
PLAYLIST_LINK = 'playlistLink'
PROMPT = 'prompt'
FILTER_PARAMS = 'filterParams'
PLAYLIST_NAME = 'playlistName'
PLAYLIST_DESCRIPTION = 'playlistDescription'
IS_PUBLIC = 'isPublic'
VALUE = 'value'
LESS_THAN_OPERATOR = '<='
GREATER_THAN_OPERATOR = '>='
REQUEST_BODY = 'requestBody'
PHOTO = 'photo'
EXISTING_PLAYLIST = 'existingPlaylist'
TIME_RANGE = "timeRange"
ACCESS_CODE_CACHE_TTL = os.getenv("ACCESS_CODE_CACHE_TTL", 30)
