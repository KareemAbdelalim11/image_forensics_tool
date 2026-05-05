from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return {}

        extracted = {}

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            extracted[tag_name] = value

        return extracted

    except Exception as e:
        print(f"Error reading EXIF: {e}")
        return {}