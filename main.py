import os
from extractor.exif_extractor import extract_exif
from gps.gps_decoder import extract_gps
from visualization.map_view import create_map
from timeline.timeline_generator import generate_timeline
from analysis.anomaly_detector import detect_anomalies
from analysis.hash_utils import calculate_hash
from reports.pdf_report import generate_pdf_report

IMAGE_FOLDER = "samples"


def main():
    all_exif = []
    locations = []
    case_data = []

    for file in os.listdir(IMAGE_FOLDER):
        path = os.path.join(IMAGE_FOLDER, file)

        print(f"\nProcessing: {file}")

        exif_data = extract_exif(path)
        gps_data = extract_gps(exif_data)
        anomalies = detect_anomalies(exif_data, path)
        file_hash = calculate_hash(path)

        if gps_data:
            locations.append(gps_data)

        all_exif.append(exif_data)

        case_data.append({
            "path": path,
            "exif": exif_data,
            "gps": gps_data,
            "anomalies": anomalies,
            "hash": file_hash
        })

        print(f"SHA-256: {file_hash}")

    # Create unified outputs
    create_map(locations)  
    generate_timeline(case_data)
    generate_pdf_report("forensic_report.pdf", case_data)


if __name__ == "__main__":
    main()