import os
from uuid import uuid4

UPLOAD_DIR = "storage/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file, prefix="image"):
    filename = f"{prefix}_{uuid4().hex}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    return filepath