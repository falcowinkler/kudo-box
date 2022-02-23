from unittest.mock import MagicMock

import flask
import pytest
import functions.write_kudo as write_kudo


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_persist_kudo(mocker):
    # Arrange
    mocker.patch("functions.write_kudo.client")
    key_mock = mocker.patch("functions.write_kudo.client.key")
    put_mock = mocker.patch("functions.write_kudo.client.put")
    entity_mock = mocker.patch("functions.write_kudo.datastore.Entity")
    entity_mock.return_value = MagicMock()
    key_mock.return_value = "some-key"

    # Act
    write_kudo.persist_kudo("team-id", "channel-id", "team-name", "channel-name", "text")

    # Assert
    key_mock.assert_called_with('Team', 'team-id', 'Channel', 'channel-id', 'Kudo')
    entity_mock.assert_called_with(key="some-key")
    entity_mock.return_value.update.assert_called_with({"text": "text"})
    put_mock.assert_called_with(entity_mock.return_value, )


def test_hello_get(app, mocker):
    mocker.patch("functions.write_kudo.persist_kudo")
    with app.test_request_context():
        res = write_kudo.write_kudo(flask.request, )
        assert 'Success' in res
