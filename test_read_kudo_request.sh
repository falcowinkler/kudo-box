#!/usr/bin/env bash

curl -s -X POST 'http://localhost:8085/v1/projects/nl-kudo-box/topics/read-kudo-queue:publish' \
    -H 'Content-Type: application/json' \
    --data '@test-read-kudo.json'
