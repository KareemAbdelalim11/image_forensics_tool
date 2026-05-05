import time
from analysis.exif_cleaner import clean_exif

def generate_report(image_path, exif_data, gps_data, anomalies):
    exif_data = clean_exif(exif_data)

    filename = f"report_{int(time.time())}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== Digital Image Forensic Report ===\n\n")

        f.write(f"Image: {image_path}\n\n")

        f.write("EXIF Metadata:\n")
        if exif_data:
            for key, value in exif_data.items():
                f.write(f"{key}: {value}\n")
        else:
            f.write("No EXIF metadata available.\n")

        f.write("\nGPS Coordinates:\n")
        f.write(f"{gps_data if gps_data else 'Not available'}\n")

        f.write("\nAnomalies Detected:\n")
        if anomalies:
            for issue in anomalies:
                f.write(f"- {issue}\n")
        else:
            f.write("No anomalies detected.\n")

    print(f"Report saved: {filename}")