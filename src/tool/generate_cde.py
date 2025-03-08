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
SEED = 42  # for reproducibility

# Desired SHC distribution (~800)
SHC_MEAN = 800.0
SHC_STD = 20.0

# Kiln feed distribution
KILN_FEED_MEAN = 160.0
KILN_FEED_STD = 10.0

# RDF feed distribution (when running)
RDF_FEED_MEAN = 120.0
RDF_FEED_STD = 5.0

# RDF NCV range
RDF_NCV_MIN = 4800
RDF_NCV_MAX = 5700

# Coal NCV (fixed)
COAL_NCV = 5500  # kcal/kg

# Clinker ratio
CLINKER_RATIO = 1.55

# Zero-rdf window in the middle
ZERO_RDF_START = START_DATE + timedelta(days=100)
ZERO_RDF_END   = ZERO_RDF_START + timedelta(days=20)  # 20-day downtime

random.seed(SEED)

# -----------------------
# Data Generation
# -----------------------
rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')

    # Is this hour in the zero-RDF window?
    in_zero_rdf = (ZERO_RDF_START <= current_time < ZERO_RDF_END)

    # 1) Intended SHC from normal dist
    shc_raw = random.normalvariate(SHC_MEAN, SHC_STD)

    # 2) Kiln feed from normal dist
    kiln_feed = max(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), 0.0)

    # 3) RDF feed & NCV
    if in_zero_rdf:
        # RDF near zero, but add small random "sensor noise"
        rdf_feed = random.uniform(0.0, 0.001)  # up to ~1 kg/h
    else:
        rdf_feed = max(random.normalvariate(RDF_FEED_MEAN, RDF_FEED_STD), 0.0)

    rdf_ncv = random.uniform(RDF_NCV_MIN, RDF_NCV_MAX)

    # 4) Calculate the total heat needed to hit the desired SHC
    #    total_heat_needed (kcal/h) = shc * (clinker_mass)
    #    clinker_mass (kg/h) = (kiln_feed * 1000) / clinker_ratio
    clinker_mass_kgph = (kiln_feed * 1000.0) / CLINKER_RATIO
    if clinker_mass_kgph <= 0:
        total_heat_needed = 0.0
    else:
        total_heat_needed = shc_raw * clinker_mass_kgph

    # 5) Heat contributed by RDF
    #    rdf_heat = (rdf_feed_t/h * 1000) * rdf_ncv
    rdf_heat = rdf_feed * 1000.0 * rdf_ncv

    # 6) Coal feed: balance the remaining heat
    #    coal_heat = total_heat_needed - rdf_heat
    #    coal_feed (t/h) = coal_heat / (1000 * coal_ncv)
    coal_heat = total_heat_needed - rdf_heat
    if coal_heat <= 0:
        # means RDF more than covers the needed heat (or no heat needed),
        # so no coal needed
        coal_feed = 0.0
        coal_heat = 0.0
    else:
        coal_feed = coal_heat / (1000.0 * COAL_NCV)

    # 7) Final recalculation of SHC from these two fuels
    #    total_heat = rdf_heat + coal_heat
    #      (we use the actual calc from feed values to ensure consistency)
    total_heat_final = (rdf_feed * 1000.0 * rdf_ncv) + (coal_feed * 1000.0 * COAL_NCV)
    if clinker_mass_kgph <= 0:
        shc_float = 0.0
    else:
        shc_float = total_heat_final / clinker_mass_kgph

    # 8) Floor the final SHC
    final_shc_int = int(math.floor(shc_float))

    # 9) Build row
    row = {
        'timestamp': ts,
        's_ph_sil_tput': kiln_feed,      # t/h of raw meal
        'f_k_coal_tput': coal_feed,      # t/h of coal
        'f_k_coal_ncv': COAL_NCV,        # can store coal ncv each row
        'f_k_rdf_tput': rdf_feed,        # t/h of RDF
        'f_k_rdf_ncv': rdf_ncv          # each hour's variable NCV
    }
    rows.append(row)

    # Store SHC only if > 0 (optional—up to you)
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
    'f_k_coal_tput',
    'f_k_coal_ncv',
    'f_k_rdf_tput',
    'f_k_rdf_ncv'
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
