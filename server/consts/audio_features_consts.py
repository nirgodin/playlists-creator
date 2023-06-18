DANCEABILITY = 'danceability'
ENERGY = 'energy'
KEY = 'key'
LOUDNESS = 'loudness'
MODE = 'mode'
SPEECHINESS = 'speechiness'
ACOUSTICNESS = 'acousticness'
INSTRUMENTALNESS = 'instrumentalness'
LIVENESS = 'liveness'
VALENCE = 'valence'
TEMPO = 'tempo'

NUMERIC_AUDIO_FEATURES = [
    ACOUSTICNESS,
    DANCEABILITY,
    ENERGY,
    INSTRUMENTALNESS,
    LIVENESS,
    LOUDNESS,
    MODE,
    SPEECHINESS,
    TEMPO,
    VALENCE
]

NON_MULTIPLIED_AUDIO_FEATURES = [
    KEY,
    MODE,
    LOUDNESS,
    TEMPO
]

MAJOR = 'major'
KEY_NAMES_MAPPING = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}
