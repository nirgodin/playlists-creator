from postgres_client.models.orm.audio_features import AudioFeatures as AudioFeaturesDB
from postgres_client.models.orm.spotify_artist import SpotifyArtist
from postgres_client.models.orm.spotify_track import SpotifyTrack
from postgres_client.postgres_utils import get_all_columns_except

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
    # TODO: Add duration to ORM and database
]

AUDIO_FEATURES_COLUMNS = get_all_columns_except(
    AudioFeaturesDB,
    AudioFeaturesDB.creation_date,
    AudioFeaturesDB.update_date
)
