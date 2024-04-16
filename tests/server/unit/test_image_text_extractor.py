from random import randint
from tempfile import TemporaryDirectory

from PIL import ImageFont, Image
from PIL.ImageDraw import Draw
from _pytest.fixtures import fixture
from flaky import flaky
from genie_common.utils import random_alphanumeric_string, compute_similarity_score, random_color

from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.utils.image_utils import current_timestamp_image_path


class TestImageTextExtractor:
    @flaky
    async def test_extract(self, extractor: ImageTextExtractor, image_path: str, text: str):
        actual = extractor.extract(image_path, "eng")
        similarity = compute_similarity_score(actual, text)
        assert similarity > 0.8

    @fixture(scope="class")
    def extractor(self) -> ImageTextExtractor:
        return ImageTextExtractor()

    @fixture(scope="class")
    def text(self) -> str:
        return random_alphanumeric_string(length=10)

    @fixture(scope="class")
    def image_path(self, image: Image) -> str:
        with TemporaryDirectory() as dir_path:
            file_path = current_timestamp_image_path(dir_path)
            image.save(file_path)

            yield file_path

    @fixture(scope="class")
    def image(self, text: str) -> Image:
        width = randint(400, 800)
        height = randint(400, 800)
        image = Image.new(
            mode='RGB',
            size=(width, height),
            color=random_color()
        )
        draw = Draw(image)
        font_size = randint(30, 50)
        font = ImageFont.load_default(font_size)
        text_width = draw.textlength(text, font=font)
        text_height = font.size
        x = randint(0, width - text_width)
        y = randint(0, height - text_height)
        draw.text(
            xy=(x, y),
            text=text,
            font=font,
            fill=random_color()
        )

        return image
