import requests
from requests import HTTPError


def get_refresh_token(event_body: dict):
    required_keys = ["refresh_token_uri", "client_id", "code", "redirect_uri", "code_verifier"]
    for key in required_keys:
        if key not in event_body:
            raise ValueError(f"Missing required key from event body: {key}")

    try:
        response = requests.post(
            url=event_body["refresh_token_uri"],
            data={
                "grant_type": "authorization_code",
                "client_id": event_body["client_id"],
                "code": event_body["code"],
                "redirect_uri": event_body["redirect_uri"],
                "code_verifier": event_body["code_verifier"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")

    return response.json()["refresh_token"]