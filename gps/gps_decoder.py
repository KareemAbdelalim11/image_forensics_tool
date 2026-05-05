def get_if_exist(data, key):
    return data[key] if key in data else None


def convert_to_degrees(value):
    def to_float(v):
        try:
            # Handles IFDRational directly
            return float(v)
        except:
            # Handles (num, denom)
            return float(v[0]) / float(v[1])

    try:
        d = to_float(value[0])
        m = to_float(value[1])
        s = to_float(value[2])
    except Exception as e:
        print("GPS format error:", e)
        return None

    return d + (m / 60.0) + (s / 3600.0)


def extract_gps(exif_data):
    gps_info = exif_data.get("GPSInfo")

    if not gps_info:
        return None

    gps_latitude = get_if_exist(gps_info, 2)
    gps_latitude_ref = get_if_exist(gps_info, 1)
    gps_longitude = get_if_exist(gps_info, 4)
    gps_longitude_ref = get_if_exist(gps_info, 3)

    # Decode bytes if needed
    if isinstance(gps_latitude_ref, bytes):
        gps_latitude_ref = gps_latitude_ref.decode()

    if isinstance(gps_longitude_ref, bytes):
        gps_longitude_ref = gps_longitude_ref.decode()

    if gps_latitude and gps_longitude:
        lat = convert_to_degrees(gps_latitude)
        lon = convert_to_degrees(gps_longitude)

        if lat is None or lon is None:
            return None

        if gps_latitude_ref != "N":
            lat = -lat

        if gps_longitude_ref != "E":
            lon = -lon

        return (lat, lon)

    return None