import base64
import json
import os
from http import HTTPStatus

import functions_framework
from google.cloud import datastore
from slack.signature import SignatureVerifier
from render.image import create_card
import random
from slack import WebClient

from google.cloud import pubsub_v1


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


client = datastore.Client()
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')


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


def process_read_kudo_request(event, context):
    message = json.loads(base64.b64decode(event['data']))
    text = message['text']
    channel = message['channel_id']
    entity_key = message['entity_key']

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
    client.delete(client.key(*entity_key))


@functions_framework.http
def read_kudo(request):
    verify_signature(request)
    channel_id = request.form["channel_id"]
    kudo_key = client.key(
        "Team",
        request.form["team_id"],
        "Channel",
        channel_id
    )
    query = client.query(kind="Kudo", ancestor=kudo_key)
    entities = list(query.fetch())
    if not entities:
        return "No more kudos", 200
    entity = entities[0]
    text = entity['text']
    entity_key = entity.key
    payload = {
        "text": text,
        "entity_key": entity_key.flat_path,
        "channel_id": channel_id
    }

    topic_path = publisher.topic_path(PROJECT_ID, "read-kudo-queue")
    message_bytes = json.dumps(payload).encode('utf-8')
    # This is what will be sent to pubsub (use for debugging in test-read-kudo-payload.json):
    # print(base64.b64encode(message_bytes))
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Drawing next kudo card...'
    except Exception as e:
        if e.code == HTTPStatus.NOT_FOUND:
            topic_name = 'projects/{project_id}/topics/{topic}'.format(
                project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
                topic='read-kudo-queue',
            )
            publisher.create_topic(name=topic_name)
            return read_kudo(request)
        print(e)
        return e, 500
