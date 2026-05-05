import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import folium
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QHBoxLayout
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from analysis.correlation import correlate_images
from extractor.exif_extractor import extract_exif
from gps.gps_decoder import extract_gps
from analysis.anomaly_detector import detect_anomalies
from analysis.hash_utils import calculate_hash
from case.case_manager import CaseManager
from reports.pdf_report import generate_pdf_report


class App(QWidget):
    def __init__(self):
        super().__init__()
        from PyQt5.QtGui import QIcon
        self.setWindowTitle("Forensic Image Analyzer Pro")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setGeometry(100, 100, 900, 750)

        self.case = CaseManager()

        # Create layout FIRST
        layout = QVBoxLayout()

        self.label = QLabel("Select or Drag Images")
        layout.addWidget(self.label)

        # Image preview
        self.image_preview = QLabel()
        layout.addWidget(self.image_preview)
        
        # Buttons
        btn_layout = QHBoxLayout()

        self.open_btn = QPushButton("Select Images")
        self.open_btn.clicked.connect(self.open_files)
        btn_layout.addWidget(self.open_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        btn_layout.addWidget(self.clear_btn)

        self.report_btn = QPushButton("Generate PDF Report")
        self.report_btn.clicked.connect(self.generate_report)
        btn_layout.addWidget(self.report_btn)

        layout.addLayout(btn_layout)

        self.output = QTextEdit()
        layout.addWidget(self.output)

        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    # File picker
    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images")
        if files:
            self.process_files(files)

    # Drag & Drop
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.process_files(files)

    # Core processing
    def process_files(self, files):
        locations = []

        for file in files:
            self.output.append(f"\n📁 {file}")

            # Show image preview
            pixmap = QPixmap(file)
            self.image_preview.setPixmap(pixmap.scaled(300, 300))

            # Extract data
            exif = extract_exif(file)
            gps = extract_gps(exif)
            anomalies = detect_anomalies(exif, file)
            file_hash = calculate_hash(file)

            # Store in case
            self.case.add_image(file, exif, gps, anomalies, file_hash)

            # Output info
            self.output.append(f"🔐 SHA-256: {file_hash}")

            if gps:
                locations.append(gps)
                self.output.append(f"📍 GPS: {gps}")
            else:
                self.output.append("📍 GPS: Not Found")

            for a in anomalies:
                self.output.append(f"⚠ {a}")

        self.update_map(locations)

        
        
    # Map
    def update_map(self, locations):
        if not locations:
            self.output.append("\n⚠ No GPS data for mapping.\n")
            return

        fmap = folium.Map(location=locations[0], zoom_start=10)

        for loc in locations:
            folium.Marker(location=loc).add_to(fmap)

        map_path = os.path.abspath("temp_map.html")
        fmap.save(map_path)

        self.map_view.load(QUrl.fromLocalFile(map_path))

    # Clear UI
    def clear_all(self):
        self.output.clear()
        self.case = CaseManager()
        self.image_preview.clear()
       
    # PDF
    def generate_report(self):
        data = self.case.get_all()

        if not data:
            self.output.append("⚠ No data to generate report.")
            return
        correlation_results = correlate_images(data)
        self.output.append("\n🔍 Correlation Analysis:")

        for r in correlation_results:
            self.output.append(f"➡ {r}")

        generate_pdf_report("forensic_report.pdf", data)
        self.output.append("✅ PDF report generated.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())