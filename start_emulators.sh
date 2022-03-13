#!/usr/bin/env bash

gcloud beta emulators datastore start &
gcloud beta emulators pubsub start &
$(gcloud beta emulators pubsub env-init)
