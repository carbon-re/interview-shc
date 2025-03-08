#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
BODY=""

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    --log-type=Tail \
    --cli-binary-format raw-in-base64-out \
    --payload='{ "plant": "bcd" }' \
    /tmp/response.json

diff <(jq --sort-keys . /tmp/response.json) <(jq --sort-keys . "$SCRIPTPATH/results/abc.expected.json")
if [ $? -eq 0 ]; then
    echo "passed!"
else
    echo "FAILED!"
    grep error /tmp/response.json
fi
