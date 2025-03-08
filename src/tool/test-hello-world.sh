#!/usr/bin/env sh

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    --log-type=TAIL \
    --payload='{"plant": "abc"}' \
    /tmp/response.json

cat /tmp/response.json
