import base64

from gift_wrap.utils.http import http


def get_token(client_id: str, client_secret: str, token_url: str):
    """
    Get an access token from cognito.
    """

    message = bytes(f"{client_id}:{client_secret}", "utf-8")
    secret_hash = base64.b64encode(message).decode()
    payload = {
        "grant_type": "client_credentials",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {secret_hash}",
    }

    resp = http.post(token_url, params=payload, headers=headers)
    return resp.json()["access_token"]
