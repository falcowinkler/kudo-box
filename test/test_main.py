import base64
import json

import flask
import pytest

import main
from persistence.gcloud import EncryptedKudo, Credentials


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


def test_process_read_kudo_request(mocker):
    # Arrange
    mocker.patch("main.delete_kudo")
    query_mock = mocker.patch('main.get_all_kudos')
    render_and_upload_kudo = mocker.patch('main.render_and_upload_kudo')
    post_initial_message = mocker.patch('main.post_initial_message')
    thread_ts = 123123
    post_initial_message.return_value = thread_ts
    query_mock.return_value = [EncryptedKudo(b"some-kudo-token", "/some/kudo/id")]
    decrypt_mock = mocker.patch('main.kudos_encryption.decrypt')
    decrypt_mock.return_value = "some-kudo-text"
    mocker.patch("os.getenv", return_value="some-password")
    payload = base64.b64encode(json.dumps({
        "channel_id": "channel-id-123",
        "team_id": "team-id-123"
    }).encode("utf-8"))
    get_credentials = mocker.patch("main.get_credentials")
    creds = Credentials(bot_token="bot-token")
    get_credentials.return_value = creds

    # Act
    main.process_read_kudo_request({"data": payload}, None)

    # Assert
    post_initial_message.assert_called_with("channel-id-123", creds, "Today's kudos in the thread 🧵!")
    render_and_upload_kudo.assert_called_with("channel-id-123", "some-kudo-text", creds, thread_ts)


def test_process_read_kudo_request_no_messages_present(mocker):
    # Arrange
    query_mock = mocker.patch('main.get_all_kudos')
    query_mock.return_value = []
    post_initial_message = mocker.patch('main.post_initial_message')
    post_initial_message.return_value = 123456
    get_credentials = mocker.patch("main.get_credentials")
    creds = Credentials(bot_token="bot-token")
    get_credentials.return_value = creds
    payload = base64.b64encode(json.dumps({
        "channel_id": "channel-id-123",
        "team_id": "team-id-123"
    }).encode("utf-8"))

    # Act
    result = main.process_read_kudo_request({"data": payload}, None)

    # Assert
    post_initial_message.assert_called_with("channel-id-123", creds,
                                            "There are no kudos in the kudo-box for this channel.")


def test_read_kudo(app, mocker):
    # Arrange
    mock_data = {
        'team_id': "team-id-123",
        'channel_id': "channel-id-123",
        'text': "some-text",
        'team_domain': "some-domain",
        'channel_name': "some-channel-name",
    }
    mocker.patch("main.get_credentials")
    mocker.patch("main.verify_signature")
    add_read_all_command_to_queue = mocker.patch('main.add_read_all_command_to_queue')

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("Drawing all kudos...", 200) == res
    add_read_all_command_to_queue.assert_called_with(
        "team-id-123", "channel-id-123"
    )


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
    mocker.patch("main.verify_signature")
    add_to_render_queue = mocker.patch('main.add_read_all_command_to_queue')
    add_to_render_queue.side_effect = Exception('error')

    # Act
    with app.test_request_context(data=mock_data):
        res = main.read_kudo(flask.request)

    # Assert
    assert ("error", 500) == res


def test_slash_command_hooks_return_authorization_error(app, mocker):
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
        res_open_kudo_box = main.open_kudo_box(flask.request)
        res_write_kudo = main.write_kudo(flask.request)
    expected_error = ("Authorization Error. "
                      f'Please <a href="{expected_link}">click here</a> to authorize.', 403)
    assert expected_error == res_write_kudo
    assert expected_error == res_open_kudo_box
