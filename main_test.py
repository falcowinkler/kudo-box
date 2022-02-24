from unittest.mock import MagicMock

import flask
import pytest

import main


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.fixture()
def client(app):
    return app.test_client()


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


def test_hello_get_returns_expected_text(app, mocker):
    # Arrange
    mocker.patch("main.persist_kudo")
    mocker.patch("main.verify_signature")
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }

    # Act
    with app.test_request_context(data=mock_data):
        res = main.write_kudo(flask.request, )

    # Assert
    assert 'Your kudo was submitted.' in res


def test_hello_persists_correct_data(app, client, mocker):
    # Arrange
    persist_mock = mocker.patch("main.persist_kudo")
    mocker.patch("main.verify_signature")
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }

    # Act
    with app.test_request_context(data=mock_data):
        res = main.write_kudo(flask.request)

    # Assert
    assert 'Your kudo was submitted.' in res
    persist_mock.assert_called_with("team-id-123", "channel-id-123", "some-domain", "some-channel-name",
                                    "some-text")
