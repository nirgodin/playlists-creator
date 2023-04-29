PROMPT_FORMAT = """
In this task you should help serialize free texts inputs that describes the characteristics of a Spotify playlist, to a 
JSON serializable string that configures the parameters that will generate this playlist.\n
The JSON string should have the following format: An array of dictionaries, each comprised by the following fields: 
column, opearator, value. There are three operators that can be used: `<` (less than), `>` (greater than) and `in` 
(included). You should not use any other operator!\n 
For example: the following text `I want a playlist of songs that are not very popular` should result in the following
JSON string: [{{"column": "popularity", "operator": "<", "value": 70}}]. In case the text also requests `Please do not
include songs that are very unpopular`, you should add to this array another dictionary: 
{{"column": "popularity", "operator": ">", "value": 70}}, and given another request to `include only songs in hebrew` you 
should add another dictionary {{"column": "language", "operator": "in", "value": ["en"]}}.\n
The possible column names (specified under `column` field) for the JSON array are:\n
1. main_genre (`in` operator)\n
2. language (`in` operator)\n
3. popularity (`<` and `>` operators)\n
4. danceability (`<` and `>` operators)\n
5. energy (`<` and `>` operators)\n
6. loudness (`<` and `>` operators)\n
7. mode (`<` and `>` operators)\n
8. speechiness (`<` and `>` operators)\n
9. acousticness (`<` and `>` operators)\n
10. instrumentalness (`<` and `>` operators)\n
11. liveness (`<` and `>` operators)\n
12. valence (`<` and `>` operators)\n
13. tempo (`<` and `>` operators)\n
Include in the JSON array only the relevant column names. For example, if you are asked for "a playlist of instrumental 
songs", your response array should include only one dictionary: [{{"column": "instrumentalness", "operator": ">", "value": 80}}]\n
Your response should include the JSON array and ONLY it. It should be serializable by a single Python `json.loads` 
command.\n
Please generate me a JSON configuration based on the following text: {user_text}
"""

SERIALIZATION_ERROR_PROMPT_FORMAT = "While serializing your response the following error occurred '{error_message}'. " \
                                    "Please regenerate a response that will avoid this exception"
