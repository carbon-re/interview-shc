#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    --log-type=Tail \
    --payload='{"plant": "cde"}' \
    --cli-binary-format raw-in-base64-out \
    --query 'LogResult' --output text \
    /tmp/response.json | base64 -d

diff -q --suppress-common-lines <(jq --sort-keys . /tmp/response.json) <(jq --sort-keys . "$SCRIPTPATH/results/cde.expected.json")
if [ $? -eq 0 ]; then
    echo "passed!"
else

    diff -y --suppress-common-lines <(jq --sort-keys . /tmp/response.json) <(jq --sort-keys . "$SCRIPTPATH/results/cde.expected.json") | head -n20
    grep error /tmp/response.json
    echo "FAILED!"
fi
