import csv
import json
import math
import random
from datetime import datetime, timedelta

# -----------------------
# Configuration
# -----------------------
START_DATE = datetime(2023, 1, 1, 0, 0)
NUM_HOURS = 24 * 6 * 30
SEED = 123

# Normal distributions
SHC_MEAN = 750.0
SHC_STD = 20.0
KILN_FEED_MEAN = 160.0
KILN_FEED_STD = 10.0

# Fixed
CLINKER_RATIO = 1.55
COAL_NCV = 6000
MIN_VALUE = 0.0

random.seed(SEED)

# -----------------------
# Generation
# -----------------------
rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    # Step 1) "Intended" SHC from normal distribution (still float)
    shc_raw = random.normalvariate(SHC_MEAN, SHC_STD)

    # Step 2) Kiln feed from normal distribution
    kiln_feed = max(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), MIN_VALUE)

    # Step 3) Back-calc coal_feed (float)
    coal_feed = (shc_raw * kiln_feed) / (COAL_NCV * CLINKER_RATIO)
    coal_feed = max(coal_feed, MIN_VALUE)

    # Step 4) Recalculate the final SHC from these floats
    #   total_heat (kcal/h) = coal_feed (t/h) * 1000 * COAL_NCV
    #   clinker_mass (kg/h) = (kiln_feed * 1000) / CLINKER_RATIO
    total_heat = coal_feed * 1000.0 * COAL_NCV
    clinker_mass = (kiln_feed * 1000.0) / CLINKER_RATIO
    shc_recalc = total_heat / clinker_mass  # float

    # Step 5) Convert to int in a stable manner
    #   e.g. floor, round, or int() to your preference
    final_shc_int = math.floor(shc_recalc)

    # Build row
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')
    row = {
        'timestamp': ts,
        's_ph_sil_tput': kiln_feed,
        'f_k_coal_tput': coal_feed,
        'f_k_coal_ncv': COAL_NCV
    }
    rows.append(row)
    shc_rows[ts] = final_shc_int

    current_time += timedelta(hours=1)

# -----------------------
# Write CSV
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

# Write expected SHCs
with open("/tmp/abc.expected.json", "w") as f:
    json.dump(shc_rows, f)

print(f"CSV file '{csv_filename}' generated with {NUM_HOURS} rows.")
