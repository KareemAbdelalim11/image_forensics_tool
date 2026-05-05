def generate_timeline(case_data):
    import pandas as pd
    import matplotlib.pyplot as plt
    from datetime import datetime
    import os

    records = []

    # ✅ Try EXIF DateTime first
    for item in case_data:
        exif = item["exif"]
        date = exif.get("DateTime") if exif else None

        if date:
            try:
                records.append(datetime.strptime(date, "%Y:%m:%d %H:%M:%S"))
            except:
                continue

    #  use file timestamps 
    if not records:
        print("⚠ No EXIF DateTime found, using file timestamps...")

        for item in case_data:
            path = item["path"]
            if os.path.exists(path):
                timestamp = os.path.getmtime(path)
                records.append(datetime.fromtimestamp(timestamp))

    if not records:
        print("❌ No timeline data found.")
        return

    df = pd.DataFrame(records, columns=["DateTime"])
    df = df.sort_values(by="DateTime")

    print("\nTimeline:")
    print(df)

    # Plot
    plt.figure()
    plt.plot(df["DateTime"], range(len(df)), marker='o')

    plt.xlabel("Time")
    plt.ylabel("Image Order")
    plt.title("Image Timeline")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("timeline.png")
    print("✅ timeline.png created")