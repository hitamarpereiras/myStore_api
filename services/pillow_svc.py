from PIL import Image
from io import BytesIO


def process_image(image, width, height):
    img = Image.open(image)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img = img.resize((width, height))

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=90, optimize=True)

    buffer.seek(0)

    return buffer, "jpg"
