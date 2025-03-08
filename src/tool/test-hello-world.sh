#!/usr/bin/env sh

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    --log-type=Tail \
    --payload='{"plant": "hello"}' \
    --cli-binary-format raw-in-base64-out \
    --query 'LogResult' --output text \
    /tmp/response.json | base64 -d

cat /tmp/response.json
