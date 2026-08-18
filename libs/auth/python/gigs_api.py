import base64
from enum import StrEnum
from typing import Iterable
from urllib.error import HTTPError

import requests


class IntegrationType(StrEnum):
    SPOTIFY = "SPOTIFY"
    TIDAL = "TIDAL"


def add_integration(
        url: str,
        user_id: str,
        encrypted_refresh_token: bytes,
        jwt: str,
        scope: str,
        integration_type: str
):
    if integration_type not in IntegrationType:
        raise ValueError(f"Invalid integration type: {integration_type}. Must be one of {list(IntegrationType)}")

    try:
        response = requests.post(
            url,
            json={
                "userId": user_id,
                "type": integration_type,
                "refreshToken": base64.b64encode(encrypted_refresh_token).decode("utf-8"),
                "scope": scope,
            },
            headers={"Authorization": jwt},
        )
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")