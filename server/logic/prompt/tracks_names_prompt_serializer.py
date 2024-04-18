from typing import Type

from server.data.track_details import TrackDetails
from server.logic.prompt.prompt_serializer_interface import IPromptSerializer


class TracksNamesPromptSerializer(IPromptSerializer):
    def build_prompt(self, user_text: str) -> str:
        return self._prompt_format.format(user_text=user_text)

    @property
    def model(self) -> Type[TrackDetails]:
        return TrackDetails

    @property
    def response_type(self) -> Type[list]:
        return list

    @property
    def _prompt_format(self) -> str:
        return """\
            In this task you should help build_prompt free texts inputs that describes the characteristics of a Spotify \
            playlist, to a JSON serializable string that specifies a list of tracks and artists names. The JSON string \
            should have the following format: An array of dictionaries, each comprised by the following fields: \
            `artist_name`, `track_name`.
            For example:
            The following text "I want a playlist of songs in the style of Eminem" should result a JSON string of the 
            following structure:
            ```
            [
                {{
                    "artist_name": "Joyner Lucas",
                    "track_name": "Darkness",
                }},
                {{
                    "artist_name": "Machine Gun Kelly",
                    "track_name": "Killshot",
                }},
                {{
                    "artist_name": "Token",
                    "track_name": "Legacy",
                }},    
            ]
            ```
            Pay attention: the example I provided to you includes only three tracks. However, in your response you \
            should include as many tracks the user requests. In case the user asks for 20 tracks, you should provide a \
            JSON serializable list with 20 entries. But be careful: No matter how many tracks the user asks, the list \
            length should not exceed 100 entries!
            Your response should include the JSON array and ONLY it. It should be serializable by a single Python \
            `json.loads` command. Please denote: the triple brackets in this prompt are used only to help you \
            distinguish code blocks. Do not include them in your response! Same goes for specifying the word `json` as \
            part of the response. Your response should always start with `[` and end with `]`.
            Please generate 50 tracks JSON list based on the following text:
            {user_text}\
        """
