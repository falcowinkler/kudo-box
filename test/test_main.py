from unittest.mock import MagicMock

import flask
import pytest

import main
from persistence.gcloud import Kudo


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.fixture()
def client(app):
    return app.test_client()


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
    with app.test_request_context(data=mock_data, content_type="multipart/form-data"):
        res = main.write_kudo(flask.request, )

    # Assert
    assert 'Your kudo was submitted.' in res


def test_hello_persists_correct_data(app, mocker):
    # Arrange
    persist_mock = mocker.patch("main.persist_kudo")
    mocker.patch("main.verify_signature")
    mocker.patch("main.verify_signature")
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }

    # Act
    with app.test_request_context(data=mock_data, content_type="multipart/form-data"):
        res = main.write_kudo(flask.request)

    # Assert
    assert 'Your kudo was submitted.' in res
    persist_mock.assert_called_with("team-id-123", "channel-id-123", "some-domain", "some-channel-name",
                                    "some-text")


def test_read_kudo(app, mocker):
    # Arrange
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    query_mock = mocker.patch('main.get_kudo')
    query_mock.return_value = Kudo("some-kudo-text", "/some/kudo/id")
    add_to_render_queue = mocker.patch('main.add_to_render_queue')
    mocker.patch("main.verify_signature")

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("Drawing next kudo...", 200) == res
    add_to_render_queue.assert_called_with("channel-id-123", Kudo("some-kudo-text", "/some/kudo/id"))


def test_read_kudo_returns_error(app, mocker):
    # Arrange
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    query_mock = mocker.patch('main.get_kudo')
    query_mock.return_value = Kudo("some-kudo-text", "/some/kudo/id")
    add_to_render_queue = mocker.patch('main.add_to_render_queue')
    add_to_render_queue.side_effect = Exception('error')
    mocker.patch("main.verify_signature")

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("error", 500) == res
