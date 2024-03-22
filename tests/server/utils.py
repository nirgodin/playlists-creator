from io import BytesIO
from typing import List, Any, Dict, Optional
from urllib.parse import urlencode

import numpy as np
from PIL import Image

from server.consts.data_consts import URI


def random_image_bytes(width: int = 1024, height: int = 1024, mode: str = "RGB", format_: str = "PNG") -> bytes:
    random_pixels = np.random.randint(255, size=(height, width, 3), dtype=np.uint8)
    image = Image.fromarray(random_pixels, mode=mode)
    image_bytes = BytesIO()
    image.save(image_bytes, format=format_)

    return image_bytes.getvalue()


def random_playlist_item(uri: str) -> Dict[str, str]:
    return {URI: uri}


def build_spotify_url(routes: List[str], params: Optional[Dict[str, Any]] = None) -> str:
    url = "https://api.spotify.com/v1"

    for route in routes:
        url += f'/{route.strip("/")}'

    if params is not None:
        return f"{url}?{urlencode(params)}"

    return url
