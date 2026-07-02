from unittest.mock import Mock

import pytest

from oauth import get_refresh_token

@pytest.fixture()
def refresh_token_event():
    return {
        "refresh_token_uri": "https://example.com/token",
        "client_id": "test_client_id",
        "code": "test_code",
        "redirect_uri": "https://example.com/callback",
        "code_verifier": "test_code_verifier"
    }


class TestGetRefreshToken:
    @pytest.mark.parametrize("key", ["refresh_token_uri", "client_id", "code", "redirect_uri", "code_verifier"])
    def test_get_refresh_token_raises_value_error_for_missing_keys(self, key, refresh_token_event):
        refresh_token_event.pop(key)
        with pytest.raises(ValueError):
            get_refresh_token(refresh_token_event)

    def test_get_refresh_token_makes_the_correct_api_call(self, mocker, refresh_token_event):
        mock_response = Mock()
        mock_response.json.return_value = {"refresh_token": "test_refresh_token"}
        mock_requests_post = mocker.patch(
            f"{get_refresh_token.__module__}.requests.post",
            return_value=mock_response,
        )

        assert get_refresh_token(refresh_token_event) == "test_refresh_token"
        mock_requests_post.assert_called_once_with(
            url="https://example.com/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "test_client_id",
                "code": "test_code",
                "redirect_uri": "https://example.com/callback",
                "code_verifier": "test_code_verifier"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )