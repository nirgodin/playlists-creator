QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT = """\
In this task you should help serialize free texts inputs that describes the characteristics of a Spotify playlist, to \
a JSON serializable string that configures the parameters that will generate this playlist. \
The JSON string should have the following format - a dictionary with two keys:
1. `musical_parameters` - describes elements regarding the musical elements of the requested playlist, such as genre, \
tempo, language, key, etc. The value of this entry should be an array of dictionaries. 
2. `textual_parameters` - presents a short summary of any non-musical element included in the free text. The value of \
this entry should should consist of one simple string.

The `musical_parameters` value should be an array of dictionaries, each comprised by the following fields: \
`column`, `operator`, `value`. There are three operators that can be used: `<=` (less than or equal to), `>=` \
(greater than or equal to) and `in` (included). You should not use any other operator!

For example:
the following text "I want a playlist of songs that are not very popular about the USA" should result in the following \
JSON string, denoted in triple brackets:
```
{{
    "musical_parameters": [
        {{
            "column": "popularity",
            "operator": "<=",
            "value": 70
        }}
    ],
    "textual_parameters": "USA"
}}
``` 
Pay attention: The musical parameters (popularity) were included in the `musical_parameters` entry, where as the \
textual parameters (USA) are in the `textual_parameters` entry. No textual parameters should be included in the \
`musical_parameters` entry!

In case the text also requests "I want a playlist of songs that are not very popular, but please do not include songs \
that are very unpopular", your response should look like this: 
```
{{
    "musical_parameters": [
        {{
            "column": "popularity",
            "operator": "<=",
            "value": 70
        }},
        {{
            "column": "popularity",
            "operator": ">=",
            "value": 30
        }} 
    ],
    "textual_parameters": null
}}
```
Pay attention: here the request to focus on USA related songs was omitted, thus no textual parameter was request. \
Because no textual parameter is mentioned in the request, you should set the value of the `textual_parameters` field \
as `null`.

Moving on to the `textual_parameters` section. Imagine the text was changed to also include a request to focus on \
songs about big cities. Now, it should look something like this: "songs about big cities that are not very popular \
nor unpopular". This request does not regard the musical elements of the playlist but to it's textual ones, meaning it \
should fall under the `textual_parameters` value. Meaning the expected response is now:
```
{{
    "musical_parameters": [
        {{
            "column": "popularity",
            "operator": "<=",
            "value": 70
        }},
        {{
            "column": "popularity",
            "operator": ">=",
            "value": 30
        }} 
    ],
    "textual_parameters": "Big cities"
}}
```
Pay attention! The `textual_parameters` field does not include any information about popularity. It extracts only the \
`textual_parameters` from the request. You should act the same.

Of course, you could also receive a request where only textual parameters are requested, and no musical element is \
mentioned. In this case, the `musical_parameters` value should be an empty array.
For example, given a text asking simply for "love songs", your response should look like this:
```
{{
    "musical_parameters": [],
    "textual_parameters": "Love"
}}
```

Hereby are specified the possible columns names of the musical parameters, along with a short description, their \
supported operators and possible values. Each column name appears right after its index, while its equivalent columns \
 details appears right below it. Each separate column section is denoted with --- separators below and above it.
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
Before returning the response, take time to think step by step how to generate the correct result. In this process, \
you should follow these steps:
1. Figure out what musical parameters are requested, and organize them to one array with the characteristics mentioned \
above. Remember! The columns names, operators and values in the `musical_parameters` array should be derived ONLY by \
the list of columns names mentioned above, and SHOULD NOT include textual column names. Please rethink before \
including any column in this array, and do not include it in case it does not appear on this list.
2. Figure out what textual parameters are requested, and summarize them to a short string. This string will be stored \
under the `musical_parameters` entry, which SHOULD NOT include any musical information.
3. Formalize these result to a single JSON dictionary. Your response should include this JSON and ONLY it. It should \
be serializable by a single Python `json.loads` command.

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
structure:
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
with 20 entries. But be careful: No matter how many tracks the user asks, the list length should not exceed 100 entries!
Your response should include the JSON array and ONLY it. It should be serializable by a single Python `json.loads` \
command. Please denote: the triple brackets in this prompt are used only to help you distinguish code blocks. Do not \
include them in your response! Same goes for specifying the word `json` as part of the response. Your response should \
always start with `[` and end with `]`.
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
