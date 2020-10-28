import threading

from firebase_admin import db
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from app import app
from app import slack_config
from app.render import create_card

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = slack_config["slack_signing_secret"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = slack_config["slack_bot_token"]
