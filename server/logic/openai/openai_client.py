import asyncio
import os
from typing import List, Dict, Optional

from aiohttp import ClientSession

from server.consts.app_consts import MESSAGE, PROMPT
from server.consts.env_consts import OPENAI_API_KEY
from server.consts.openai_consts import CHAT_COMPLETIONS_URL, MODEL, MESSAGES, GPT_3_5_TURBO, CHOICES, CONTENT, \
    IMAGE_SIZE_512, DATA, URL, CREATED, N, SIZE, IMAGES_GENERATION_URL, IMAGE, IMAGES_VARIATIONS_URL
from server.utils.image_utils import save_image_from_url


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

    async def create_image(self, prompt: str, image_path: str) -> Optional[str]:
        body = {
            PROMPT: prompt,
            N: 1,
            SIZE: IMAGE_SIZE_512
        }

        async with self._session.post(url=IMAGES_GENERATION_URL, json=body, headers=self._headers) as raw_response:
            raw_response.raise_for_status()
            response = await raw_response.json()

        return await self._save_result(response, image_path)

    async def variate_image(self, original_image_path: str, image_path: str) -> Optional[str]:
        body = {
            IMAGE: open(original_image_path, 'rb'),
            N: 1,
            SIZE: IMAGE_SIZE_512
        }

        async with self._session.post(url=IMAGES_VARIATIONS_URL, json=body, headers=self._headers) as raw_response:
            raw_response.raise_for_status()
            response = await raw_response.json()

        return await self._save_result(response, image_path)

    async def _save_result(self, response: dict, image_path: str) -> Optional[str]:
        image_url = response[DATA][0][URL]
        image_creation_timestamp = response[CREATED]
        file_name = f'{image_creation_timestamp}.png'
        original_image_dir_path = os.path.dirname(image_path)
        created_image_path = os.path.join(original_image_dir_path, file_name)
        await save_image_from_url(self._session, image_url, created_image_path)

        if os.path.exists(image_path):
            return created_image_path


if __name__ == '__main__':
    messages = [{'role': 'user', 'content': 'Are you working?'}]
    client = OpenAIClient(ClientSession())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.chat_completions(messages))
