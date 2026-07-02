import pytest

from jwt import get_requesting_user


class TestGetRequestingUser:
    def test_get_requesting_user_returns_user_id_from_jwt_claims(self):
        event = {
            "requestContext": {
                "authorizer": {
                    "jwt": {
                        "claims": {
                            "sub": "123"
                        }
                    }
                }
            }
        }

        assert get_requesting_user(event) == "USER#123"

    @pytest.mark.parametrize(
        "event",
        [
            {},
            {"requestContext": {}},
            {"requestContext": {"authorizer": {}}},
            {"requestContext": {"authorizer": {"jwt": {}}}},
            {"requestContext": {"authorizer": {"jwt": {"claims": {}}}}}
        ]
    )
    def test_get_requesting_user_returns_empty_string_if_no_jwt_claims(self, event):
        event = {}
        assert get_requesting_user(event) == ""