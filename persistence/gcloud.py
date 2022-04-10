import random
from collections import namedtuple

from google.cloud import datastore

EncryptedKudo = namedtuple("EncryptedKudo", ["token", "key"])
Credentials = namedtuple("Credentials", ["bot_token"])

client = datastore.Client()


def persist_kudo(team_id, channel_id, token):
    kudo_key = client.key("Team", team_id, "Channel", channel_id, "Kudo")
    entity = datastore.Entity(key=kudo_key)
    entity.update({
        "token": token
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
    return EncryptedKudo(entity['token'], entity.key.flat_path)


def delete_kudo(kudo_key):
    client.delete(client.key(*kudo_key))


def get_bot_token(team_id):
    bot_key = client.key("Team", team_id)
    query = client.query(kind="Credentials", ancestor=bot_key)

    entities = list(query.fetch())
    if not entities:
        raise Exception("No credentials found")
    entity = entities[0]

    return Credentials(entity['bot_token'])


def persist_bot_token(team_id, bot_token):
    return
