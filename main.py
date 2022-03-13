import os

import functions_framework
from google.cloud import datastore
from slack.signature import SignatureVerifier
from render.image import create_card
import random
from slack import WebClient


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


client = datastore.Client()


def persist_kudo(team_id, channel_id, team_name, channel_name, text):
    kudo_key = client.key("Team", team_id, "Channel", channel_id, "Kudo")
    entity = datastore.Entity(key=kudo_key)
    entity.update({
        "text": text
    })
    client.put(entity)


@functions_framework.http
def write_kudo(request):
    verify_signature(request)
    persist_kudo(
        request.form['team_id'],
        request.form['channel_id'],
        request.form['team_domain'],
        request.form["channel_name"],
        request.form["text"])
    return 'Your kudo was submitted.'


def random_title():
    return random.choice([
        "Here's a sticker",
        "Sorry, you don't get a medal though",
        "Makes a great wall decoration!",
        "You get this designer-approved card!",
        "You get this tacky card as a reward.",
        "+5 jollity",
        "Show it to all your friends!",
        "Consider the environment before printing.",
        "For your trophy collection:"
    ])


def random_comment():
    return random.choice([
        "Good job!",
        "Way to go, kiddo",
        "WTG!",
        "What would we do without you",
        "Great success!",
        "Nice!",
        "Noice!",
        "Sweet",
        "Dandy",
        "Sweet n' dandy"
    ])


@functions_framework.http
def read_kudo(request):
    channel = request.form["channel_id"]
    kudo_key = client.key(
        "Team",
        request.form["team_id"],
        "Channel",
        channel
    )
    query = client.query(kind="Kudo", ancestor=kudo_key)
    entities = list(query.fetch())
    if not entities:
        return "Error", 500
    entity = entities[0]
    text = entity["text"]
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
    client.delete(entity.key)
    return 200
