import cv2
import numpy as np
from numpy import ndarray
from pytesseract import image_to_string


class ImageTextExtractor:
    def extract(self, image_path: str, language: str = "eng") -> str:
        image = cv2.imread(image_path)
        pre_processed_image = self._pre_process_image(image)
        text = image_to_string(pre_processed_image, lang=language, config='--psm 6')

        return text.rstrip("\n")

    @staticmethod
    def _pre_process_image(image: ndarray) -> ndarray:
        original = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 120, 0])
        upper = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask == 0] = (255, 255, 255)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        return cv2.threshold(result, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
