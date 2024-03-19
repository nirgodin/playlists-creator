from io import BytesIO

import numpy as np
from PIL import Image


def generate_random_image_bytes(width: int = 1024, height: int = 1024, mode: str = "RGB", format_: str = "PNG") -> bytes:
    random_pixels = np.random.randint(255, size=(height, width, 3), dtype=np.uint8)
    image = Image.fromarray(random_pixels, mode=mode)
    image_bytes = BytesIO()
    image.save(image_bytes, format=format_)

    return image_bytes.getvalue()
