import folium

def create_map(locations):
    if not locations:
        print("No GPS data found.")
        return

    fmap = folium.Map(location=locations[0], zoom_start=10)

    for loc in locations:
        folium.Marker(location=loc).add_to(fmap)

    fmap.save("map.html")
    print("Map saved as map.html")