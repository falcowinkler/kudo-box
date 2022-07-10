import json
import os
from http import HTTPStatus

from google.cloud import pubsub_v1

publisher = None
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')


def add_to_render_queue(channel_id, kudo, team_id):
    global publisher
    if publisher is None:
        publisher = pubsub_v1.PublisherClient()
    payload = {
        "text": kudo.text,
        "entity_key": kudo.key,
        "channel_id": channel_id,
        "team_id": team_id
    }
    topic_path = publisher.topic_path(PROJECT_ID, "read-kudo-queue")
    message_bytes = json.dumps(payload).encode('utf-8')
    # This is what will be sent to pubsub (use for debugging in test-read-kudo-payload.json):
    # print(base64.b64encode(message_bytes))
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
    except Exception as e:
        if e.code == HTTPStatus.NOT_FOUND:
            topic_name = 'projects/{project_id}/topics/{topic}'.format(
                project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
                topic='read-kudo-queue',
            )
            publisher.create_topic(name=topic_name)
            return add_to_render_queue(channel_id, kudo, team_id)
        raise e
