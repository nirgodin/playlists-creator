import asyncio
import os
from typing import List, Dict

from aiohttp import ClientSession

from server.consts.app_consts import MESSAGE
from server.consts.env_consts import OPENAI_API_KEY
from server.consts.openai_consts import CHAT_COMPLETIONS_URL, MODEL, MESSAGES, GPT_3_5_TURBO, CHOICES, CONTENT


class OpenAIClient:
    def __init__(self, session: ClientSession):
        self._session = session
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ[OPENAI_API_KEY]}'
        }

    async def chat_completions(self, messages: List[Dict[str, str]]) -> str:
        body = {
            MODEL: GPT_3_5_TURBO,
            MESSAGES: messages
        }

        async with self._session.post(url=CHAT_COMPLETIONS_URL, json=body, headers=self._headers) as raw_response:
            raw_response.raise_for_status()
            response = await raw_response.json()

        return response[CHOICES][0][MESSAGE][CONTENT]


if __name__ == '__main__':
    messages = [{'role': 'user', 'content': 'Are you working?'}]
    client = OpenAIClient(ClientSession())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.chat_completions(messages))
