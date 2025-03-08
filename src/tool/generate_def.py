import csv
import json
import math
import random
from datetime import datetime, timedelta

#
# -----------------------
# Configuration
# -----------------------
#

START_DATE = datetime(2025, 1, 1, 0, 0)   # Starting timestamp
NUM_DAYS = 5                              # e.g., 5 days of data
NUM_HOURS = 24 * NUM_DAYS
SEED = 42

# SHC distribution
SHC_MEAN = 800.0
SHC_STD = 20.0

# Kiln feed distribution
KILN_FEED_MEAN = 160.0
KILN_FEED_STD = 10.0

# RDF feed distribution: typically around 8-12 t/h
RDF_FEED_MIN = 8.0
RDF_FEED_MAX = 12.0

# RDF NCV range in GJ/ton (matching ~4800-5700 kcal/kg)
RDF_NCV_MIN_GJPT = 20.1
RDF_NCV_MAX_GJPT = 23.9

# Petcoke NCV (fixed, in kcal/kg)
PETCOKE_NCV = 7600.0

# Clinker ratio
CLINKER_RATIO = 1.55

# Zero-RDF window to simulate downtime
ZERO_RDF_START = START_DATE + timedelta(days=1)  # Day 1 to day 2
ZERO_RDF_END   = ZERO_RDF_START + timedelta(days=1)

# For reproducibility
random.seed(SEED)

#
# -----------------------
# Data Generation
# -----------------------
#

rows = []
shc_rows = {}
current_time = START_DATE

for i in range(NUM_HOURS):
    # Timestamp
    ts = current_time.strftime('%Y-%m-%d %H:%M:%S')
    current_time_dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

    in_zero_rdf_window = (ZERO_RDF_START <= current_time_dt < ZERO_RDF_END)

    # 1) "Intended" SHC from normal distribution (center ~800)
    shc_raw = random.normalvariate(SHC_MEAN, SHC_STD)

    # 2) Kiln feed from normal distribution
    kiln_feed = max(random.normalvariate(KILN_FEED_MEAN, KILN_FEED_STD), 0.0)

    # 3) RDF feed in t/h
    if in_zero_rdf_window:
        # near zero with sensor noise
        rdf_feed = random.uniform(0.0, 0.001)
    else:
        rdf_feed = random.uniform(RDF_FEED_MIN, RDF_FEED_MAX)

    # 4) RDF NCV in GJ/ton
    rdf_ncv_gjpt = random.uniform(RDF_NCV_MIN_GJPT, RDF_NCV_MAX_GJPT)
    # Convert GJ/ton -> kcal/kg
    #    1 GJ/ton = 239 kcal/kg (approx)
    rdf_ncv_kcalpkg = rdf_ncv_gjpt * 239.0

    # 5) Calculate total heat needed to achieve SHC
    #    clinker_mass (kg/h) = (kiln_feed * 1000) / clinker_ratio
    clinker_mass_kgph = (kiln_feed * 1000.0) / CLINKER_RATIO if kiln_feed > 0 else 0.0
    if clinker_mass_kgph <= 0:
        total_heat_needed = 0.0
    else:
        total_heat_needed = shc_raw * clinker_mass_kgph  # kcal/h

    # 6) Heat contributed by RDF
    #    rdf_heat (kcal/h) = rdf_feed(t/h) * 1000(kg/t) * rdf_ncv_kcalpkg(kcal/kg)
    rdf_heat_kcalph = rdf_feed * 1000.0 * rdf_ncv_kcalpkg

    # 7) Petcoke feed to balance the remaining heat
    #    petcoke_heat_needed = total_heat_needed - rdf_heat_kcalph
    #    petcoke_feed (t/h) = petcoke_heat_needed / (1000 kg/t * PETCOKE_NCV)
    petcoke_heat_kcalph = total_heat_needed - rdf_heat_kcalph
    if petcoke_heat_kcalph <= 0:
        # RDF alone covers needed heat
        petcoke_feed = 0.0
        petcoke_heat_kcalph = 0.0
    else:
        petcoke_feed = petcoke_heat_kcalph / (1000.0 * PETCOKE_NCV)

    # 8) Final SHC from these fuels
    total_heat_final = rdf_heat_kcalph + (petcoke_feed * 1000.0 * PETCOKE_NCV)
    if clinker_mass_kgph <= 0:
        shc_float = 0.0
    else:
        shc_float = total_heat_final / clinker_mass_kgph

    # 9) Floor the SHC
    final_shc_int = int(math.floor(shc_float))

    #
    # Build row data
    #
    row = {
        'timestamp': ts,
        'kiln_feed_tph': kiln_feed,
        'f_k_rdf_tput': rdf_feed,
        'f_k_rdf_ncv': rdf_ncv_gjpt,  # store in GJ/ton
        'f_k_petcoke_tput': petcoke_feed,
        'f_k_petcoke_ncv': PETCOKE_NCV,    # kcal/kg
    }
    rows.append(row)

    # Save SHC if > 0 (optional)
    if final_shc_int > 0:
        shc_rows[ts] = final_shc_int

    # Advance one hour
    current_time += timedelta(hours=1)


#
# -----------------------
# Write CSV
# -----------------------
#
csv_filename = '/tmp/def.csv'
fieldnames = [
    'timestamp',
    'kiln_feed_tph',
    'f_k_rdf_tput',
    'f_k_rdf_ncv',
    'f_k_petcoke_tput',
    'f_k_petcoke_ncv'
]

with open(csv_filename, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

#
# -----------------------
# Write JSON of final SHC
# -----------------------
#
json_filename = '/tmp/def.expected.json'
with open(json_filename, 'w') as f:
    json.dump(shc_rows, f)

print(f"Generated '{csv_filename}' with {NUM_HOURS} rows.")
print(f"Generated matching SHC data in '{json_filename}'.")
