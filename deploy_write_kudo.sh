gcloud functions deploy write_kudo \
--runtime python39 \
--trigger-http \
--set-env-vars "SLACK_SECRET=YOUR_SLACK_SIGNING_SECRET,KG_API_KEY=YOUR_KG_API_KEY" \
--allow-unauthenticated