from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from sqlalchemy import Row

from server.consts.api_consts import ID
from server.consts.data_consts import RELEASE_DATE, EXPLICIT
from server.database.database_models.artist import Artist
from server.database.database_models.audio_features import AudioFeatures
from server.database.database_models.lyrics import Lyrics


@dataclass_json
@dataclass
class Track:
    id: str
    explicit: bool
    release_date: datetime
    audio_features: AudioFeatures
    lyrics: Lyrics
    artist: Artist

    def __post_init__(self):
        self.release_year = self.release_date.year

    @classmethod
    def from_row(cls, row: Row) -> "Track":
        jsonified_row = dict(row._mapping)
        return cls(
            id=jsonified_row[ID],
            release_date=jsonified_row[RELEASE_DATE],
            explicit=jsonified_row[EXPLICIT],
            audio_features=AudioFeatures.from_dict(jsonified_row),
            lyrics=Lyrics.from_dict(jsonified_row),
            artist=Artist.from_dict(jsonified_row)
        )

    def to_record(self) -> dict:
        record = {}

        for field in fields(self):
            field_value = getattr(self, field.name)

            if is_dataclass(field_value):
                record.update(field_value.to_dict())
            else:
                record[field.name] = field_value

        return record
