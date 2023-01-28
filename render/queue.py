import json
import os

from google.cloud import pubsub_v1

COMMAND_READ_ONE = "read_one"
COMMAND_READ_ALL = "read_all"

publisher = None
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')


def create_read_kudo_topic():
    global publisher
    if publisher is None:
        publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=PROJECT_ID,
        topic='read-kudo-queue',
    )
    publisher.create_topic(name=topic_name)


def add_read_all_command_to_queue(team_id, channel_id):
    payload = {
        "command": COMMAND_READ_ALL,
        "channel_id": channel_id,
        "team_id": team_id
    }
    add_payload_to_render_queue(payload)


def add_to_render_queue(channel_id, kudo, team_id):
    payload = {
        "command": COMMAND_READ_ONE,
        "text": kudo.text,
        "entity_key": kudo.key,
        "channel_id": channel_id,
        "team_id": team_id
    }
    add_payload_to_render_queue(payload)


def add_payload_to_render_queue(payload):
    global publisher
    if publisher is None:
        publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, "read-kudo-queue")
    message_bytes = json.dumps(payload).encode('utf-8')
    # This is what will be sent to pubsub (use for debugging in test-read-kudo-payload.json):
    # print(base64.b64encode(message_bytes))

    publish_future = publisher.publish(topic_path, data=message_bytes)
    publish_future.result()  # Verify the publish succeeded
