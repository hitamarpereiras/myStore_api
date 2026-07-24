from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(file):

    MAX_IMAGE_SIZE = 1 * 1024 * 1024

    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError("Imagem muito grande! Máximo de 1MB")
    
    # Verifica se realmente é uma imagem
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("O Arquivo não é uma imagem válida")