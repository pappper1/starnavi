import io

from fastapi import UploadFile
from PIL import Image


async def is_image(file: UploadFile) -> bool:
    try:
        image = Image.open(io.BytesIO(file.file.read()))
        image.verify()

        return True
    except (IOError, SyntaxError):
        return False
