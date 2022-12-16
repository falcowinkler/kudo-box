#!/usr/bin/env bash

curl -s -X PUT 'http://localhost:8085/v1/projects/nl-kudo-box/topics/read-kudo-queue'

#curl -s -X PUT 'http://localhost:8085/v1/projects/nl-kudo-box/subscriptions/read-kudo-queue' \
#    -H 'Content-Type: application/json' \
#    --data '{"topic":"projects/nl-kudo-box/topics/read-kudo-queue","pushConfig":{"pushEndpoint":"http://localhost:8081"}}'

curl -X POST 'http://localhost:8085/v1/projects/nl-kudo-box/topics/read-kudo-queue:publish' \
    -H 'Content-Type: application/json' \
    --data '@test-read-kudo.json'
