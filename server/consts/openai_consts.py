from server.consts.data_consts import SONG, URI, NAME, ARTIST_NAME, GENRES, MAIN_ALBUM

PROMPT_PREFIX_FORMAT = """\
In this task you should help serialize free texts inputs that describes the characteristics of a Spotify playlist, to \
a JSON serializable string that configures the parameters that will generate this playlist. \
The JSON string should have the following format: An array of dictionaries, each comprised by the following fields: \
`column`, `opearator`, `value`. There are three operators that can be used: `<` (less than), `>` (greater than) and \
`in` (included). You should not use any other operator!
For example:
the following text "I want a playlist of songs that are not very popular" should result in the following JSON string, \
denoted in triple brackets:
```
[
    {{
        "column": "popularity",
        "operator": "<",
        "value": 70
    }}
]
```
In case the text also requests "Please do not include songs that are very unpopular", you should add to the following \
dictionary to the mentioned array: 
```
{{
    "column": "popularity",
    "operator": ">",
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
In case of an "in" operator, all possible values included in the string are supported. In case of "< or >" operator, \
the list parentheses represents a close range, where the first value denotes the column minimum possible value, and \
the second value denotes the column max value. You may return any number inside this range, depend on the user input. \
The possible column names for the JSON array are:
{columns_details}
"""

PROMPT_SUFFIX_FORMAT = """\
Include in the JSON array only relevant column names. For example, if you are asked for "a playlist of instrumental \
songs", your response should include an array with only one dictionary:
```
[
    {{
        "column": "instrumentalness",
        "operator": ">",
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

EXCLUDED_COLUMNS = [
    SONG,
    NAME,
    ARTIST_NAME,
    URI,
    GENRES,
    MAIN_ALBUM
]
IN_OPERATOR = 'in'
NUMERIC_OPERATORS = '< or >'
SINGLE_COLUMN_DESCRIPTION_FORMAT = """\
{column_index}. {column_name}
---
operator: {column_operator}
values: {column_values}
---
"""
