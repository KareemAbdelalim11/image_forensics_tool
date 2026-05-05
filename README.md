# 🔍 Digital Image Forensic Analyzer

A professional desktop application for extracting, analyzing, and visualizing hidden metadata (EXIF) from digital images.  
Designed for forensic investigations to reveal image origin, location, timeline, and possible manipulation.

---

## 📌 Overview

Digital images often contain hidden metadata such as:

- 📍 GPS location  
- 🕒 Timestamp  
- 📱 Camera model  
- 🛠 Software used  

This tool helps investigators extract and analyze this data to reconstruct events and detect anomalies.

---

## 🚀 Features

- 🔎 EXIF Metadata Extraction  
- 🌍 GPS Coordinate Decoding  
- 📊 Timeline Analysis (with fallback support)  
- 🔗 Image Correlation (time + location)  
- ⚠️ Anomaly Detection (missing/edited metadata)  
- 🔐 SHA-256 Hashing (evidence integrity)  
- 🗺️ Interactive Map Visualization  
- 📄 PDF Forensic Report Generation  
- 🖥️ User-Friendly GUI (PyQt5)  
- 📦 Standalone `.exe` Application  


## 🧠 System Workflow
Image → EXIF Extraction → GPS Decoding → Anomaly Detection
↓
Case Management
↓
Map Visualization + Timeline Analysis
↓
Correlation Engine
↓
PDF Forensic Report


## 📦 Download Executable

Download the ready-to-use application:

👉 https://drive.google.com/file/d/1XrCIqek-U2ZMcOs-EPJLV507zsmv0lDO/view?usp=sharing


## ⚙️ Setup Instructions 

1️⃣ Clone Repository

git clone <https://github.com/KareemAbdelalim11/image_forensics_tool.git>
cd image-forensics-tool

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Application
python -m gui.app


## 🖥️ How to Use
1. Load Images
    . Click Select Images
    . Or drag & drop images into the app

2. Automatic Analysis
The system will:
    . Extract EXIF metadata
    . Decode GPS (if available)
    . Generate SHA-256 hash
    . Detect anomalies

3. View Results
Displayed in GUI:
    📁 Image path
    🔐 Hash
    📍 GPS location
    ⚠️ Detected issues

4. Generate Report
Click:
    "Generate PDF Report"

This produces:
    "forensic_report.pdf"

## 📄 Report Includes
    Metadata analysis
    GPS coordinates
    Anomaly detection
    Correlation results
    Timeline visualization
    Hash values


## ⚠️ Known Limitations
    Cannot recover removed metadata
    GPS only works if saved in EXIF
    Timeline depends on timestamp availability


## 👨‍💻 Author
    Kareem Mohamed