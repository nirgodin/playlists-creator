import pandas as pd
from pandas import DataFrame

from server.consts.data_consts import ALBUM_NAME, TRACK_NAME, TRACK_URI, ARTIST_NAME, RELEASE_YEAR, RELEASE_DATE
from server.utils.regex_utils import extract_year

METADATA_COLUMNS = [
    ALBUM_NAME,
    TRACK_NAME,
    ARTIST_NAME
]
ID_COLUMNS = [
    TRACK_URI
]


class PlaylistDetailsPipeline:
    def transform(self, data: DataFrame) -> DataFrame:
        data[RELEASE_YEAR] = [extract_year(date) for date in data[RELEASE_DATE]]
        # data[MAIN_GENRE] =



if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/Downloads/serialized_playlist_details.csv')
    PlaylistDetailsPipeline().transform(data)
