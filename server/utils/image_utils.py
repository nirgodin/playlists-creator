import requests
import io
from PIL import Image


def save_image(image_url: str, output_path: str) -> None:
    response = requests.get(image_url)

    if response.status_code != 200:
        print("Failed to download the image.")
        return

    image_bytes = response.content
    file = io.BytesIO(image_bytes)
    image = Image.open(file)
    image.save(output_path)
    print("Successfully saved image")
