import csv
import json
import math
import random
from datetime import datetime, timedelta

# -----------------------
# Configuration
# -----------------------
START_DATE = datetime(2023, 1, 1, 0, 0)
NUM_DAYS = 365
NUM_HOURS = 24 * NUM_DAYS
SEED = 234

# Normal distributions for non-zero window
SHC_MEAN = 750.0
SHC_STD = 20.0
KILN_FEED_MEAN = 160.0
KILN_FEED_STD = 10.0

# Fixed constants
CLINKER_RATIO = 1.55
COAL_NCV = 5500  # kcal/kg (still used in calculations, only shown in first row)
MIN_VALUE = 0.0

# Zero-production period: a 30-day window in the middle
start_of_zero = START_DATE + timedelta(days=150)
end_of_zero   = start_of_zero + timedelta(days=30)

random.seed(SEED)

# -----------------------
# Data Generation
# -----------------------
rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')
    in_zero_window = (start_of_zero <= current_time < end_of_zero)

    # --------------------------
    # 1) "Intended" SHC
    # --------------------------
    if in_zero_window:
        # We'll set "intended" SHC to 0 if in zero window
        shc_raw = 0.0
    else:
        # Normal distribution around 750 +/- 20
        shc_raw = random.normalvariate(SHC_MEAN, SHC_STD)

    # --------------------------
    # 2) Kiln feed
    # --------------------------
    if in_zero_window:
        # Add a small random epsilon to simulate near-zero sensor noise, in t/h
        kiln_feed = random.uniform(0.0, 0.001)  # up to ~1 kg/h
        coal_feed = random.uniform(0.0, 0.0001)  # up to ~0.1 kg/h
    else:
        kiln_feed = max(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), MIN_VALUE)
        coal_feed = (shc_raw * kiln_feed) / (COAL_NCV * CLINKER_RATIO)
        coal_feed = max(coal_feed, MIN_VALUE)

    # --------------------------
    # 4) Recalculate final SHC from these floats
    # --------------------------
    total_heat = coal_feed * 1000.0 * COAL_NCV
    clinker_mass = (kiln_feed * 1000.0) / CLINKER_RATIO

    if clinker_mass <= 0.0:
        # Avoid dividing by zero
        shc_recalc_float = 0.0
    else:
        shc_recalc_float = total_heat / clinker_mass

    # --------------------------
    # 5) Floor the SHC
    # --------------------------
    final_shc_int = int(math.floor(shc_recalc_float))

    # Build row for CSV
    ncv_for_this_row = COAL_NCV if (i == 0) else ""  # only show NCV in first row
    row = {
        'timestamp': ts,
        's_ph_sil_tput': kiln_feed,    # t/h
        'f_k_coal_tput': coal_feed,    # t/h
        'f_k_coal_ncv': ncv_for_this_row
    }
    rows.append(row)

    # Only store SHC if it's > 0
    if not in_zero_window:
        shc_rows[ts] = final_shc_int

    current_time += timedelta(hours=1)

# -----------------------
# Write CSV
# -----------------------
csv_filename = '/tmp/abc_coal_ncv_firstrow.csv'
with open(csv_filename, mode='w', newline='') as f:
    fieldnames = ['timestamp', 's_ph_sil_tput', 'f_k_coal_tput', 'f_k_coal_ncv']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

# Write expected SHCs (skipping SHC=0)
with open("/tmp/abc_coal_ncv_firstrow.expected.json", "w") as f:
    json.dump(shc_rows, f)

print(f"CSV file '{csv_filename}' generated with {NUM_HOURS} rows.")
print(" - One-month near-zero-production period with random epsilon feed.")
print(" - NCV only on first row.")
print(" - Only storing SHC>0 in the JSON.")
