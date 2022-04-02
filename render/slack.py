import os

from slack import WebClient

from render.image import create_card
from render.text import random_title, random_comment


def upload_kudo(channel, text):
    file_path = create_card(text)
    slack_bot_token = os.environ['SLACK_BOT_TOKEN']
    slack_client = WebClient(token=slack_bot_token)
    slack_client.api_call("files.upload",
                          files={
                              "file": file_path
                          },
                          data={
                              'channels': channel,
                              'filename': "kudos.png",
                              'title': random_title(),
                              'initial_comment': random_comment(),
                          }
                          )