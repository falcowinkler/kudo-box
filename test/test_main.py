import flask
import pytest

import main
from persistence.gcloud import EncryptedKudo


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.fixture()
def client(app):
    return app.test_client()


def test_write_kudo_returns_expected_test(app, mocker):
    # Arrange
    mocker.patch("main.persist_kudo")
    mocker.patch("main.get_credentials")
    mocker.patch("main.verify_signature")
    mocker.patch("os.getenv").return_value = "server-side-secret"
    encryption_mock = mocker.patch("main.kudos_encryption.encrypt")
    encryption_mock.return_value = b"some-kudo-token"
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
    assert res == 'Your kudo got created in the box for #some-channel-name'


def test_write_kudo_persists_correct_data(app, mocker):
    # Arrange
    persist_mock = mocker.patch("main.persist_kudo")
    mocker.patch("main.verify_signature")
    mocker.patch("main.get_credentials")
    mocker.patch("os.getenv").return_value = "server-side-secret"
    encryption_mock = mocker.patch("main.kudos_encryption.encrypt")
    encryption_mock.return_value = b"some-kudo-token"
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }

    # Act
    with app.test_request_context(data=mock_data, content_type="multipart/form-data"):
        main.write_kudo(flask.request)

    # Assert
    persist_mock.assert_called_with("team-id-123", "channel-id-123",
                                    b"some-kudo-token")


def test_read_kudo(app, mocker):
    # Arrange
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    decrypt_mock = mocker.patch('main.kudos_encryption.decrypt')
    decrypt_mock.return_value = "some-kudo-text"
    mocker.patch("main.get_credentials")
    query_mock = mocker.patch('main.get_kudo')
    query_mock.return_value = EncryptedKudo(b"some-kudo-token", "/some/kudo/id")
    add_to_render_queue = mocker.patch('main.add_to_render_queue')
    mocker.patch("main.verify_signature")
    mocker.patch("os.getenv", return_value="some-password")

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("Drawing next kudo...", 200) == res
    add_to_render_queue.assert_called_with("channel-id-123", main.Kudo("some-kudo-text", "/some/kudo/id"),
                                           'team-id-123')
    decrypt_mock.assert_called_with(b"some-kudo-token", "some-password")


def test_read_kudo_returns_error(app, mocker):
    # Arrange
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    mocker.patch("main.get_credentials")
    query_mock = mocker.patch('main.get_kudo')
    query_mock.return_value = EncryptedKudo(b"some-kudo-token", "/some/kudo/id")
    decrypt_mock = mocker.patch('main.kudos_encryption.decrypt')
    decrypt_mock.return_value = "some-kudo-text"
    add_to_render_queue = mocker.patch('main.add_to_render_queue')
    add_to_render_queue.side_effect = Exception('error')
    mocker.patch("main.verify_signature")

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("error", 500) == res


def test_read_kudo_returns_authorization_error(app, mocker):
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    mocker.patch("main.verify_signature")
    get_credentials = mocker.patch("main.get_credentials")
    get_credentials.return_value = None
    getenv = mocker.patch('os.getenv')
    getenv.return_value = "slack-client-id"
    scopes = "channels:join,chat:write,commands,files:write"
    expected_link = f"https://some-domain.slack.com/oauth/v2/authorize?client_id=slack-client-id&scope={scopes}"
    with app.test_request_context(data=mock_data):
        res_read_kudo = main.read_kudo(flask.request)
        res_write_kudo = main.read_kudo(flask.request)
    expected_error = ("Authorization Error. "
                      f'Please <a href="{expected_link}">click here</a> to authorize.', 403)
    assert expected_error == res_write_kudo
    assert expected_error == res_read_kudo
