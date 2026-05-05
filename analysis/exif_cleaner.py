def clean_exif(exif_data):
    important_fields = [
        "Make",
        "Model",
        "DateTime",
        "Software"
    ]

    cleaned = {}

    for key, value in exif_data.items():
        # Skip binary
        if isinstance(value, bytes):
            continue

        # Keep only important fields
        if key in important_fields:
            cleaned[key] = value

    return cleaned