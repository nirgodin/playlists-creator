from aiohttp import ClientSession

from server.consts.api_consts import AUDIO_FEATURES_URL_FORMAT


class AudioFeaturesCollector:
    def __init__(self, session: ClientSession):
        self._session = session

    async def collect(self, track_id: str) -> dict:
        url = AUDIO_FEATURES_URL_FORMAT.format(track_id)

        async with self._session.get(url=url) as response:
            return await response.json()
