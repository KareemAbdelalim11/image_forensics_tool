from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from analysis.exif_cleaner import clean_exif
from analysis.correlation import correlate_images
from reportlab.platypus import Image
import os
from timeline.timeline_generator import generate_timeline

def generate_pdf_report(filename, case_data):
    generate_timeline(case_data)
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("DIGITAL IMAGE FORENSIC REPORT", styles["Title"]))
    content.append(Spacer(1, 20))

    for idx, item in enumerate(case_data, start=1):
        exif = clean_exif(item["exif"])

        # Section header
        content.append(Paragraph(f"--- Evidence #{idx} ---", styles["Heading2"]))
        content.append(Spacer(1, 10))

        # Image path
        content.append(Paragraph(f"<b>File:</b> {item['path']}", styles["Normal"]))
        content.append(Spacer(1, 10))

        # HASH
        content.append(Paragraph("<b>Integrity (SHA-256):</b>", styles["Heading3"]))
        content.append(Paragraph(item["hash"], styles["Normal"]))
        content.append(Spacer(1, 10))

        # EXIF SECTION
        content.append(Paragraph("<b>Metadata Analysis:</b>", styles["Heading3"]))

        if exif:
            for k, v in exif.items():
                content.append(Paragraph(f"{k}: {v}", styles["Normal"]))
        else:
            content.append(Paragraph("No relevant EXIF metadata found.", styles["Normal"]))

        content.append(Spacer(1, 10))

        # GPS SECTION
        content.append(Paragraph("<b>Geolocation:</b>", styles["Heading3"]))
        if item["gps"]:
            content.append(Paragraph(f"Latitude/Longitude: {item['gps']}", styles["Normal"]))
        else:
            content.append(Paragraph("No GPS data available.", styles["Normal"]))

        content.append(Spacer(1, 10))

        # ANOMALIES SECTION
        content.append(Paragraph("<b>Forensic Observations:</b>", styles["Heading3"]))

        if item["anomalies"]:
            for a in item["anomalies"]:
                content.append(Paragraph(f"- {a}", styles["Normal"]))
        else:
            content.append(Paragraph("No anomalies detected.", styles["Normal"]))

        content.append(Spacer(1, 20))

    content.append(Paragraph("Correlation Analysis", styles["Heading2"]))
    correlation_results = correlate_images(case_data)
    if correlation_results:
        for r in correlation_results:
            content.append(Paragraph(r, styles["Normal"]))
    else:
        content.append(Paragraph("No correlation detected.", styles["Normal"]))        
    
    content.append(Spacer(1, 20))
    if os.path.exists("timeline.png"):
        content.append(Paragraph("Timeline Visualization", styles["Heading2"]))
        content.append(Spacer(1, 10))
        content.append(Image("timeline.png", width=400, height=300))
        content.append(Spacer(1, 20))


    doc.build(content)