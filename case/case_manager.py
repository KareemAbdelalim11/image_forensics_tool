class CaseManager:
    def __init__(self):
        self.images = []

    def add_image(self, path, exif, gps, anomalies, file_hash):
        self.images.append({
            "path": path,
            "exif": exif,
            "gps": gps,
            "anomalies": anomalies,
            "hash": file_hash
        })

    def get_all(self):
        return self.images