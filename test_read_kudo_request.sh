#!/usr/bin/env bash


curl -d "@test-read-kudo.json" \
  -X POST \
  -H "Content-Type: application/json" \
  http://localhost:8080