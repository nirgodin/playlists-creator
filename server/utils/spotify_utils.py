from server.consts.data_consts import ITEMS, TRACKS


def extract_tracks_from_response(playlist: dict) -> list:
    return playlist.get(TRACKS, {}).get(ITEMS, [])
