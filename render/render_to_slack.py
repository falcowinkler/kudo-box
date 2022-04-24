from slack import WebClient

from render.image import create_card
from render.text import random_title, random_comment


def render_and_upload_kudo(channel, text, credentials):
    file_path = create_card(text)
    slack_client = WebClient(token=credentials.bot_token)
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