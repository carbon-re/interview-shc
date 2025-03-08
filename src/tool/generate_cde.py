import csv
import json
import math
import random
from datetime import datetime, timedelta

# -----------------------
# Configuration
# -----------------------
START_DATE = datetime(2023, 1, 1, 0, 0)
NUM_DAYS = 60  # e.g., 2 months of data, adjust as needed
NUM_HOURS = 24 * NUM_DAYS
SEED = 42  # for reproducibility

# Desired SHC distribution (~800)
SHC_MEAN = 800.0
SHC_STD = 20.0

# Kiln feed distribution
KILN_FEED_MEAN = 160.0
KILN_FEED_STD = 10.0

# RDF feed: normally in [8, 12]
RDF_FEED_MIN = 8.0
RDF_FEED_MAX = 12.0

# RDF NCV range
RDF_NCV_MIN = 4800.0
RDF_NCV_MAX = 5700.0

# Coal NCV (fixed)
COAL_NCV = 5500.0  # kcal/kg

# Clinker ratio
CLINKER_RATIO = 1.55

# Zero-RDF window
ZERO_RDF_START = START_DATE + timedelta(days=20)  # day 20 to 25, for example
ZERO_RDF_END   = ZERO_RDF_START + timedelta(days=5)

random.seed(SEED)

# -----------------------
# Data Generation
# -----------------------
rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')
    in_zero_rdf = (ZERO_RDF_START <= current_time < ZERO_RDF_END)

    # 1) Intended SHC from normal dist (around 800 ± 20)
    shc_raw = random.normalvariate(SHC_MEAN, SHC_STD)

    # 2) Kiln feed from normal dist
    kiln_feed = max(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), 0.0)

    # 3) RDF feed
    if in_zero_rdf:
        # If in zero window, near zero with sensor noise up to 0.001 t/h
        rdf_feed = random.uniform(0.0, 0.001)
    else:
        # Normally between 8 and 12 t/h
        rdf_feed = random.uniform(RDF_FEED_MIN, RDF_FEED_MAX)

    # 4) RDF NCV for this hour
    rdf_ncv = random.uniform(RDF_NCV_MIN, RDF_NCV_MAX)

    # 5) Calculate total heat needed to meet desired SHC
    #    clinker_mass (kg/h) = (kiln_feed * 1000) / clinker_ratio
    clinker_mass_kgph = (kiln_feed * 1000.0) / CLINKER_RATIO
    if clinker_mass_kgph <= 0:
        total_heat_needed = 0.0
    else:
        total_heat_needed = shc_raw * clinker_mass_kgph

    # 6) Heat contributed by RDF
    #    rdf_heat = rdf_feed(t/h)*1000 kg/t * rdf_ncv(kcal/kg)
    rdf_heat = rdf_feed * 1000.0 * rdf_ncv

    # 7) Coal feed is whatever is needed to meet total_heat_needed
    coal_heat = total_heat_needed - rdf_heat
    if coal_heat <= 0:
        # Means RDF alone covers or exceeds needed heat
        coal_feed = 0.0
        coal_heat = 0.0
    else:
        # coal_feed (t/h) = coal_heat / (1000 kg/t * coal_ncv(kcal/kg))
        coal_feed = coal_heat / (1000.0 * COAL_NCV)

    # 8) Final SHC check (from these two fuels)
    total_heat_final = rdf_heat + (coal_feed * 1000.0 * COAL_NCV)
    if clinker_mass_kgph <= 0:
        shc_float = 0.0
    else:
        shc_float = total_heat_final / clinker_mass_kgph

    # 9) Floor final SHC
    final_shc_int = int(math.floor(shc_float))

    # Build row for CSV
    row = {
        'timestamp': ts,
        's_ph_sil_tput': kiln_feed,   # t/h raw meal
        'f_k_rdf_tput': rdf_feed,     # t/h RDF
        'f_k_rdf_ncv': rdf_ncv,       # variable NCV
        'f_k_coal_tput': coal_feed,   # t/h coal (balancing energy)
        'f_k_coal_ncv': COAL_NCV      # fixed
    }
    rows.append(row)

    # Store SHC if > 0 (optional)
    if final_shc_int > 0:
        shc_rows[ts] = final_shc_int

    current_time += timedelta(hours=1)

# -----------------------
# Write CSV
# -----------------------
csv_filename = '/tmp/cde.csv'
fieldnames = [
    'timestamp',
    's_ph_sil_tput',
    'f_k_rdf_tput',
    'f_k_rdf_ncv',
    'f_k_coal_tput',
    'f_k_coal_ncv'
]

with open(csv_filename, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

# -----------------------
# Write JSON of final SHC
# -----------------------
json_filename = '/tmp/cde.expected.json'
with open(json_filename, 'w') as f:
    json.dump(shc_rows, f)

print(f"Generated '{csv_filename}' with {NUM_HOURS} rows.")
print(f"Generated matching SHC data in '{json_filename}'.")
