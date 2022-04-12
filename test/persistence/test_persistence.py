from unittest.mock import MagicMock
from persistence.gcloud import Credentials

import persistence.gcloud


def test_persist_kudo(mocker):
    # Arrange
    mocker.patch("persistence.gcloud.client")
    key_mock = mocker.patch("persistence.gcloud.client.key")
    put_mock = mocker.patch("persistence.gcloud.client.put")
    entity_mock = mocker.patch("persistence.gcloud.datastore.Entity")
    entity_mock.return_value = MagicMock()
    key_mock.return_value = "some-key"

    # Act
    persistence.gcloud.persist_kudo("team-id", "channel-id", b"some-kudo-token")

    # Assert
    key_mock.assert_called_with('Team', 'team-id', 'Channel', 'channel-id', 'Kudo')
    entity_mock.assert_called_with(key="some-key")
    entity_mock.return_value.update.assert_called_with({"token": b"some-kudo-token"})
    put_mock.assert_called_with(entity_mock.return_value, )


def test_get_bot_token(mocker):
    # Arrange
    mocker.patch("persistence.gcloud.client")
    client_query_mock = mocker.patch("persistence.gcloud.client.query")
    query_mock = MagicMock()
    client_query_mock.return_value = query_mock
    query_mock.fetch.return_value = [{"bot_token": "abc-123"}]

    # Act
    result = persistence.gcloud.get_bot_token("team-id")

    # Assert
    assert result == Credentials("abc-123")


def test_persist_bot_token(mocker):
    # Arrange
    mocker.patch("persistence.gcloud.client")
    key_mock = mocker.patch("persistence.gcloud.client.key")
    put_mock = mocker.patch("persistence.gcloud.client.put")
    entity_mock = mocker.patch("persistence.gcloud.datastore.Entity")
    entity_mock.return_value = MagicMock()
    key_mock.return_value = "some-key"

    # Act
    persistence.gcloud.persist_bot_token("team-id", b"some-bot-token")

    # Assert
    key_mock.assert_called_with('Team', 'team-id', 'Credentials')
    entity_mock.assert_called_with(key="some-key")
    entity_mock.return_value.update.assert_called_with({"bot_token": b"some-bot-token"})
    put_mock.assert_called_with(entity_mock.return_value, )
