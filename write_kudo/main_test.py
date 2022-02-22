from unittest.mock import MagicMock

import flask
import pytest
import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_persist_kudo(mocker):
    # Arrange
    mocker.patch("main.client")
    key_mock = mocker.patch("main.client.key")
    put_mock = mocker.patch("main.client.put")
    entity_mock = mocker.patch("main.datastore.Entity")
    entity_mock.return_value = MagicMock()
    key_mock.return_value = "some-key"

    # Act
    main.persist_kudo("team-id", "channel-id", "team-name", "channel-name", "text")

    # Assert
    key_mock.assert_called_with('Team', 'team-id', 'Channel', 'channel-id', 'Kudo')
    entity_mock.assert_called_with(key="some-key")
    entity_mock.return_value.update.assert_called_with({"text": "text"})
    put_mock.assert_called_with(entity_mock.return_value, )


def test_hello_get(app, mocker):
    persistence_mock = mocker.patch("main.persist_kudo")
    with app.test_request_context():
        res = main.write_kudo(flask.request, )
        assert 'Success' in res