import secrets
import string
import uuid
from pathlib import Path
from PIL import Image
from flask import current_app
from app.models import WaterReport

def generate_reference_code() -> str:
    """
    Generate a cryptographically random, non-sequential reference code.
    Format: JR-XXXXXXXXXX (e.g., JR-K7B4N9X2QW)
    Ensures uniqueness against database records.
    """
    # Exclude easily confused characters like O, 0, I, 1
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    while True:
        suffix = ''.join(secrets.choice(alphabet) for _ in range(10))
        code = f"JR-{suffix}"
        # Check database for collision
        existing = WaterReport.query.filter_by(reference_code=code).first()
        if not existing:
            return code


def save_uploaded_photo(file_storage) -> str | None:
    """
    Safely save an uploaded photograph:
    - Verifies extension
    - Validates image content using Pillow
    - Saves with a random UUID-based filename outside static/
    Returns the saved filename, or None if invalid.
    """
    if not file_storage or not file_storage.filename:
        return None
    
    filename = file_storage.filename.lower()
    ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''
    
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'webp'})
    if ext not in allowed:
        return None
    
    # Secure random filename
    random_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(parents=True, exist_ok=True)
    target_path = upload_folder / random_filename

    try:
        # Validate that the file is an actual readable image using Pillow
        image = Image.open(file_storage)
        image.verify()  # verify that it is an image
        
        # Rewind file pointer and save safely
        file_storage.seek(0)
        file_storage.save(target_path)
        return random_filename
    except Exception:
        # If invalid or corrupted image, reject
        if target_path.exists():
            target_path.unlink()
        return None


def sanitize_csv_field(value) -> str:
    """
    Neutralize CSV / spreadsheet formula injection attacks.
    If a string starts with =, +, -, @, \t, or \r, prefix with a single quote.
    """
    if value is None:
        return ""
    text = str(value).strip()
    if text and text[0] in ('=', '+', '-', '@', '\t', '\r'):
        return f"'{text}"
    return text
