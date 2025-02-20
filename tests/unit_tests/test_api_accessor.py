from unittest import mock

from server.api.api_accessor import SessionManager
from server.config import config


async def test_session_manager(mocker):
    class MockSession(mock.Mock):
        fetch_token = mock.AsyncMock()
        refresh_tokens = mock.AsyncMock()

        is_expired = mock.Mock(return_value=True)
        has_refresh_token = mock.Mock(return_value=False)

    manager = SessionManager()
    mocker.patch("server.api.api_accessor.OAuth2Session", MockSession)

    session = await manager.get_session()
    assert session
    session.fetch_token.assert_called_once()


async def test_api_get(api_accessor):
    result = await api_accessor.api_get("test")
    api_accessor.api_session.session.request.assert_called_once_with(
        "GET",
        config.API_BASE_URL + "test"
    )

    assert result == (200, "test")


async def test_api_patch(api_accessor):
    data = dict()
    result = await api_accessor.api_patch("test", data)
    api_accessor.api_session.session.request.assert_called_once_with(
        "PATCH",
        config.API_BASE_URL + "test",
        headers={"Content-type": "application/json"},
        json=data
    )

    assert result == (200, "test")


async def test_update_achievements(api_accessor):
    achievements = await api_accessor.update_achievements([dict(
        achievement_id="test",
        update_type="test"
    )], 1)
    assert achievements == (200, "test")


async def test_update_events(api_accessor):
    events = await api_accessor.update_events([dict(
        event_id="test"
    )], 1)
    assert events == (200, "test")
