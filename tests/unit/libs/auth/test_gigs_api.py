from unittest.mock import Mock

import pytest

from gigs_api import add_integration


class TestAddIntegration:
    def test_add_integration_makes_the_correct_api_call(self, mocker):
        mock_requests_post = mocker.patch(
            f"{add_integration.__module__}.requests.post",
            return_value=Mock(),
        )

        add_integration(
            url="https://example.com/integrations",
            user_id="test_user_id",
            encrypted_refresh_token=b"test_encrypted_refresh_token",
            jwt="test_jwt",
            scope=["test_scope"],
            integration_type="SPOTIFY"
        )

        mock_requests_post.assert_called_once_with(
            "https://example.com/integrations",
            json={
                "userId": "test_user_id",
                "type": "SPOTIFY",
                "refreshToken": "dGVzdF9lbmNyeXB0ZWRfcmVmcmVzaF90b2tlbg==",
                "scope": ["test_scope"],
            },
            headers={"Authorization": "test_jwt"},
        )

    def test_add_integration_raises_value_error_if_invalid_integration_type_given(self):
        with pytest.raises(ValueError):
            add_integration(
                url="https://example.com/integrations",
                user_id="test_user_id",
                encrypted_refresh_token=b"test_encrypted_refresh_token",
                jwt="test_jwt",
                scope=["test_scope"],
                integration_type="INVALID_INTEGRATION_TYPE"
            )
