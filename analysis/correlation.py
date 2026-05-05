from datetime import datetime
import math

# Distance between two GPS points (km)
def calculate_distance(coord1, coord2):
    if not coord1 or not coord2:
        return None

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
    except:
        return None


def correlate_images(case_data):
    correlated = []

    # Extract usable data
    for item in case_data:
        exif = item["exif"]

        dt = parse_datetime(exif.get("DateTime", "")) if exif else None
        gps = item["gps"]

        correlated.append({
            "path": item["path"],
            "time": dt,
            "gps": gps
        })

    # Sort by time
    correlated = [x for x in correlated if x["time"]]
    correlated.sort(key=lambda x: x["time"])

    results = []

    # Compare consecutive images
    for i in range(len(correlated) - 1):
        current = correlated[i]
        next_img = correlated[i + 1]

        time_diff = (next_img["time"] - current["time"]).total_seconds() / 60  # minutes
        distance = calculate_distance(current["gps"], next_img["gps"])

        if distance is not None:
            if distance < 0.001:
                results.append(
                    f"Same location detected between {current['path']} and {next_img['path']}"
                )
            else:
                results.append(
                    f"Movement detected: {current['path']} → {next_img['path']} | Distance: {distance:.4f} | Time: {time_diff:.1f} min"
                )
        else:
            results.append(
                f"No GPS correlation between {current['path']} and {next_img['path']}"
            )

    return results