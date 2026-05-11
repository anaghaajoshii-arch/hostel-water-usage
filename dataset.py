import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# 15 hostel blocks
blocks = [f"Block_{i}" for i in range(1, 16)]

rows = []

start = datetime(2026, 5, 1, 0, 0)

# Generate 7 days of hourly data
for day in range(7):

    for hour in range(24):

        current_time = start + timedelta(days=day, hours=hour)

        for block in blocks:

            # Peak usage hours
            if 5 <= hour <= 9:
                base = np.random.randint(250, 450)

            elif 17 <= hour <= 22:
                base = np.random.randint(220, 400)

            elif 0 <= hour <= 4:
                base = np.random.randint(50, 120)

            else:
                base = np.random.randint(120, 250)

            students = np.random.randint(180, 500)

            leakage = round(np.random.uniform(1, 8), 2)

            usage = round(base + np.random.normal(0, 20), 2)

            rows.append([
                current_time.date(),
                current_time.hour,
                block,
                students,
                max(usage, 30),
                leakage
            ])

df = pd.DataFrame(rows, columns=[
    "Date",
    "Hour",
    "Hostel_Block",
    "Students",
    "Water_Usage",
    "Leakage_Percentage"
])

print(df.head())

df.to_csv("hostel_hourly_water_usage.csv", index=False)