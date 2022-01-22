import os
import json

with open(os.getenv("CONFIG_FILE"), "r") as config_file:
    config = json.load(config_file)
    config["slackConfig"] = {
        "slack_signing_secret": os.getenv("SLACK_SIGNING_SECRET"),
        "slack_bot_token": os.getenv("SLACK_BOT_TOKEN"),
    }
