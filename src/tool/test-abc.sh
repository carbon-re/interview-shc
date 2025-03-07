#!/usr/bin/env sh

aws lambda invoke \
    --function-name shc-calculator \
    --region=eu-west-1 \
    /tmp/response.json

diff /tmp/response.json abc.expected.json
