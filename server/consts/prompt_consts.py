QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT = """\
In this task you should help serialize free texts inputs that describes the characteristics of a Spotify playlist, to \
a JSON serializable string that configures the parameters that will generate this playlist. \
The JSON string should have the following format: An array of dictionaries, each comprised by the following fields: \
`column`, `opearator`, `value`. There are three operators that can be used: `<=` (less than or equal to), `>=` \
(greater than or equal to) and `in` (included). You should not use any other operator!
For example:
the following text "I want a playlist of songs that are not very popular" should result in the following JSON string, \
denoted in triple brackets:
```
[
    {{
        "column": "popularity",
        "operator": "<=",
        "value": 70
    }}
]
```
In case the text also requests "Please do not include songs that are very unpopular", you should add to the following \
dictionary to the mentioned array: 
```
{{
    "column": "popularity",
    "operator": ">=",
    "value": 30
}} 
```
Given another request to "include only songs in hebrew" you should add another dictionary:
{{
    "column": "language",
    "operator": "in",
    "value": ["en"]
}}
```
Hereby are specified the possible columns names, along with a short description, their supported operators and \
possible values. Each column name appears right after its index, while its equivalent columns details appears right \
below it. Each separate column section is denoted with --- separators below and above it.
For example:
12. artist_gender
---
operator: in
values: ['band', 'female', 'male']
description: The possible gender of the artists included in the playlist
---
In case of an "in" operator, all possible values included in the string are supported. In case of "<= or >=" operator, \
the list parentheses represents a close range, where the first value denotes the column minimum possible value, and \
the second value denotes the column max value. You may return any number inside this range, depend on the user input. \
The possible column names for the JSON array are:
{columns_details}
"""

QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT = """\
Include in the JSON array only relevant column names. For example, if you are asked for "a playlist of instrumental \
songs", your response should include an array with only one dictionary:
```
[
    {{
        "column": "instrumentalness",
        "operator": ">=",
        "value": 80
    }}
]
```
Your response should include the JSON array and ONLY it. It should be serializable by a single Python `json.loads` \
command.
Please generate a JSON configuration based on the following text:
{user_text}\
"""

SERIALIZATION_ERROR_PROMPT_FORMAT = """\
While serializing your response the following error occurred
```
{error_message}
```
Please regenerate a response that will avoid this exception.
"""

SINGLE_COLUMN_DESCRIPTION_FORMAT = """\
{column_index}. {column_name}
---
operator: {column_operator}
values: {column_values}
description: {column_description}
---
"""


TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT = """\
In this task you should help serialize free texts inputs that describes the characteristics of a Spotify playlist, to \
a JSON serializable string that specifies a list of tracks and artists names. \
The JSON string should have the following format: An array of dictionaries, each comprised by the following fields: \
`artist_name`, `track_name`.
For example:
The following text "I want a playlist of songs in the style of Eminem" should result a JSON string of the following, \
structure, denoted in triple brackets:
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
Pay attention: the example I provided to you includes only three tracks. However, in your response you should include \
as many tracks the user requests. In case the user asks for 20 tracks, you should provide a JSON serializable list \
with 20 entries. Pay attention: No matter how many tracks the user asks, the list length should not exceed 100 entries!
Your response should include the JSON array and ONLY it. It should be serializable by a single Python `json.loads` \
command.
Please generate 50 tracks JSON list based on the following text:
{user_text}\
"""

PHOTO_ARTISTS_PROMPT_PREFIX = """\
Please extract from the following text, denoted in triple brackets, all music artists names you can find. You should \
return the names in a JSON serializable array, where each entry contains a single artist name. Your response should 
include the JSON array and ONLY it. It should be serializable by a single `json.loads` command. For example, \
given the following text:
```
EMINEM: tric Bry ili bopgameempiiges Kid cudi LAROI-Charfi Ruj-dmc, ~
```
Your response should look like this:
```
[
    eminem,
    kid cudi,
    run dmc
]
```
 
In case you do not detect any artists name in the text, return an empty array. Remember: You should return ONLY JSON \
serializable string, and nothing else.
Please generate artists names JSON list based on the following text:
"""
