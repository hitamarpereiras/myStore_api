from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime
import os
import uuid

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


if not url or not key:
    raise ValueError("Supabase não configurado")

supabase = create_client(url, key)

def upload_image(file_bytes, ext, bucket):
    SUPABASE_BUCKET = bucket

    date = datetime.now().strftime("%d%m%Y_%H%M%S")
    name_image = f"{date}_{uuid.uuid4().hex[:8]}.{ext}"
    path_storage = f"public/{name_image}"

    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path_storage,
            file_bytes,
            file_options={"content-type": f"image/{ext}"}
        )
    except Exception as e:
        raise Exception(f"Erro ao fazer o upload: {str(e)}")
    
    url_publica = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path_storage)
    
    return {
        "url": url_publica,
        "path": path_storage
    }


def delete_image(path, bucket):
    SUPABESE_BUCKET = bucket

    try:
        supabase.storage.from_(SUPABESE_BUCKET).remove([path])
        return True
    except Exception as e:
        return False