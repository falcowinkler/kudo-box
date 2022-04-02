import random
from collections import namedtuple

from google.cloud import datastore

Kudo = namedtuple("Kudo", ["text", "key"])

client = datastore.Client()


def persist_kudo(team_id, channel_id, team_name, channel_name, text):
    kudo_key = client.key("Team", team_id, "Channel", channel_id, "Kudo")
    entity = datastore.Entity(key=kudo_key)
    entity.update({
        "text": text
    })
    client.put(entity)


def get_kudo(team_id, channel_id):
    """returns random (text, key) if any kudo exists in the box or None otherwise."""
    kudo_key = client.key(
        "Team",
        team_id,
        "Channel",
        channel_id
    )
    query = client.query(kind="Kudo", ancestor=kudo_key)
    entities = list(query.fetch())
    if not entities:
        return
    entity = random.choice(entities)
    return Kudo(entity['text'], entity.key.flat_path)


def delete_kudo(kudo_key):
    client.delete(client.key(*kudo_key))
