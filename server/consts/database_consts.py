from genie_datastores.postgres.models import (
    AudioFeatures as AudioFeaturesDB,
    RadioTrack,
    SpotifyArtist,
    SpotifyTrack
)
from genie_datastores.postgres.utils import get_all_columns_except
from sqlalchemy import func

from server.consts.data_consts import POPULARITY, ARTIST_POPULARITY, ARTIST_FOLLOWERS

ARTIST_COLUMNS = [
    SpotifyArtist.id.label(f"spotify_{SpotifyTrack.artist_id.key}"),
    SpotifyArtist.gender,
    SpotifyArtist.genres,
    SpotifyArtist.primary_genre,
    SpotifyArtist.is_israeli,
]

TRACK_COLUMNS = [
    SpotifyTrack.id,
    SpotifyTrack.artist_id,
    SpotifyTrack.explicit,
    SpotifyTrack.release_date,
]

AUDIO_FEATURES_COLUMNS = get_all_columns_except(
    AudioFeaturesDB,
    AudioFeaturesDB.creation_date,
    AudioFeaturesDB.update_date
)

RADIO_TRACK_COLUMNS = [
    RadioTrack.track_id,
    func.avg(RadioTrack.popularity).label(POPULARITY),
    func.avg(RadioTrack.artist_popularity).label(ARTIST_POPULARITY),
    func.avg(RadioTrack.artist_followers).label(ARTIST_FOLLOWERS),
]
