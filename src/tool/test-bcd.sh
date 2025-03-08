#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    --log-type=Tail \
    --payload='{"plant": "bcd"}' \
    --cli-binary-format raw-in-base64-out \
    /tmp/response.json

diff <(jq --sort-keys . /tmp/response.json) <(jq --sort-keys . "$SCRIPTPATH/results/bcd.expected.json")
if [ $? -eq 0 ]; then
    echo "passed!"
else
    echo "FAILED!"
fi
