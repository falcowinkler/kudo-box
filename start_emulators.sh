#!/usr/bin/env bash

gcloud beta emulators datastore start &
gcloud beta emulators pubsub start --project=nl-kudo-box --host-port='localhost:8085' &
$(gcloud beta emulators pubsub env-init)
