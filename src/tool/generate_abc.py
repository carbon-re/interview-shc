import csv
import json
import random
from datetime import datetime, timedelta

# -----------------------
# Configuration
# -----------------------
START_DATE = datetime(2023, 1, 1, 0, 0)  # Starting timestamp
NUM_HOURS = 24 * 6 * 30                  # Number of hourly rows
SEED = 123                               # For reproducibility (optional)

# For the normal distributions
SHC_MEAN = 750.0       # kcal/kg
SHC_STD = 20.0         # e.g., ±20 around 750
KILN_FEED_MEAN = 160.0 # t/h
KILN_FEED_STD = 10.0

# Fixed parameters
CLINKER_RATIO = 1.55
COAL_NCV = 6000        # kcal/kg
MIN_VALUE = 0.0        # clamp to zero to avoid negative feeds

# Ensure repeatable random numbers (optional)
random.seed(SEED)

# -----------------------
# Data Generation
# -----------------------
rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    # 1) Select an SHC from normal distribution (in ~700-800 range)
    shc = round(random.normalvariate(SHC_MEAN, SHC_STD), 2)

    # 2) Select a kiln feed from normal distribution
    kiln_feed = round(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), 2)
    # Clamp negative
    kiln_feed = max(kiln_feed, MIN_VALUE)

    # 3) Back-calculate the coal feed to achieve that SHC
    #    coalFeed = (SHC * kilnFeed) / (NCV * clinkerRatio)
    coal_feed = (shc * kiln_feed) / (COAL_NCV * CLINKER_RATIO)
    coal_feed = max(coal_feed, MIN_VALUE)

    # Build row
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')
    row = {
        'timestamp': ts,
        's_ph_sil_tput': round(kiln_feed, 2),    # t/h
        'f_k_coal_tput': round(coal_feed, 2),    # t/h
        'f_k_coal_ncv': COAL_NCV,               # kcal/kg
    }

    rows.append(row)
    shc_rows[ts] = int(shc)
    current_time += timedelta(hours=1)

# -----------------------
# Write to CSV
# -----------------------
csv_filename = '/tmp/abc.csv'
with open(csv_filename, mode='w', newline='') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=['timestamp', 's_ph_sil_tput', 'f_k_coal_tput', 'f_k_coal_ncv']
    )
    writer.writeheader()
    for r in rows:
        writer.writerow(r)


with open("/tmp/abc.expected.json", "w") as f:
    json.dump(shc_rows, f)

print(f"CSV file '{csv_filename}' generated with {NUM_HOURS} rows.")
