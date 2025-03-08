#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    /tmp/response.json

diff <(jq --sort-keys . /tmp/response.json) <(jq --sort-keys . "$SCRIPTPATH/results/abc.expected.json")
if [ $? -eq 0 ]; then
    echo "passed!"
else
    echo "FAILED!"
    cat /tmp/response.json
fi
