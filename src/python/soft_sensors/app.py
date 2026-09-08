#!/usr/bin/env python3
"""
Read a plant CSV from S3 and print its specific heat consumption as JSON.

    python -m src.python.soft_sensors.app abc
    python -m src.python.soft_sensors.app abc --bucket cre-data-shc-20250908
    python -m src.python.soft_sensors.app abc --local-dir src/infra/plant-data
"""

import argparse
import json
import os
import pathlib
import sys

import pandas as pd

from src.python.soft_sensors.shc import ShcSoftSensor

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Terraform creates the data bucket with `bucket_prefix = "cre-data-shc"`, so the
# full name carries a random suffix and can only be resolved at runtime.
BUCKET_PREFIX = "cre-data-shc"


def find_bucket(prefix: str = BUCKET_PREFIX) -> str:
    """
    Return the name of the plant-data bucket.

    Prefers $PLANT_DATA_BUCKET, otherwise looks for the single bucket in the
    account whose name starts with the terraform bucket prefix.
    """
    bucket = os.environ.get("PLANT_DATA_BUCKET")
    if bucket:
        return bucket

    import boto3

    buckets = [
        b["Name"]
        for b in boto3.client("s3").list_buckets()["Buckets"]
        if b["Name"].startswith(prefix)
    ]

    if not buckets:
        raise RuntimeError(
            f"no bucket found starting with {prefix!r}. Deploy it with "
            "`terraform -chdir=src/infra apply`, or pass --bucket / set "
            "$PLANT_DATA_BUCKET."
        )
    if len(buckets) > 1:
        raise RuntimeError(
            f"found several candidate buckets ({', '.join(sorted(buckets))}); "
            "pass --bucket to choose one."
        )

    return buckets[0]


def read_plant_data(plant: str, bucket: str | None = None) -> pd.DataFrame:
    """Read a plant's CSV from the root of the S3 data bucket."""
    import awswrangler as wr

    bucket = bucket or find_bucket()
    return wr.s3.read_csv(f"s3://{bucket}/{plant}.csv")


def calculate_shc(raw_data: pd.DataFrame) -> dict[str, int]:
    """Calculate SHC for every row of plant data, keyed by timestamp."""
    sensor = ShcSoftSensor()
    result = sensor.calculate(sensor.transform(raw_data))

    shc = result["shc"].dropna()
    return {
        timestamp.strftime(TIMESTAMP_FORMAT): int(value)
        for timestamp, value in shc.items()
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plant", help="plant code, eg. abc")
    parser.add_argument(
        "--bucket",
        help=f"S3 bucket holding the plant CSVs (default: discovered by the "
        f"{BUCKET_PREFIX!r} prefix, or $PLANT_DATA_BUCKET)",
    )
    parser.add_argument(
        "--local-dir",
        type=pathlib.Path,
        help="read from this local directory instead of S3, for offline runs",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation; use 0 for a single line",
    )
    args = parser.parse_args(argv)

    if args.local_dir:
        csv_path = args.local_dir / f"{args.plant}.csv"
        if not csv_path.is_file():
            parser.error(f"no such CSV file: {csv_path}")
        raw_data = pd.read_csv(csv_path)
    else:
        raw_data = read_plant_data(args.plant, args.bucket)

    print(json.dumps(calculate_shc(raw_data), indent=args.indent or None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
