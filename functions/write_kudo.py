# [START functions_write_kudo]
import functions_framework
from google.cloud import datastore

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
    """Responds to any HTTP request.
        Args:
            request (flask.Request): HTTP request object.
        Returns:
            The response text or any set of values that can be turned into a
            Response object using
            `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
        """
    persist_kudo("team_id", "channel_id", "team_name", "channel_name", "text")
    return f'Success'
# [END functions_write_kudo]
