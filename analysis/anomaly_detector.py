import os
from datetime import datetime

def detect_anomalies(exif_data, image_path=None):
    issues = []

    if not exif_data:
        issues.append("No EXIF metadata -> likely WhatsApp or social media compression.")

    # Detect suspicious software
    if "Software" in exif_data:
        software = str(exif_data["Software"]).lower()
        if "whatsapp" in software:
            issues.append("Image processed by WhatsApp.")

    # File name hint
    if image_path:
        filename = os.path.basename(image_path).lower()
        if "img-" in filename or "whatsapp" in filename:
            issues.append("Filename suggests WhatsApp origin.")

        # File timestamp fallback
        timestamp = os.path.getmtime(image_path)
        dt = datetime.fromtimestamp(timestamp)
        issues.append(f"File system timestamp: {dt}")

    if "GPSInfo" not in exif_data:
        issues.append("GPS data missing -> cannot determine location.")

    return issues