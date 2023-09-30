from fastapi.testclient import TestClient

from sapphire.common.api.schemas import ResponseStatus
from sapphire.users.jwt import JWTMethods


def test_issue_tokens_without_user_id(test_client: TestClient):
    resp = test_client.get("/api/v1beta/oauth2/habr")
    assert resp.status_code == 200
    assert resp.json().get("status") == ResponseStatus.ERROR


def test_issue_tokens_with_user_id(test_client: TestClient, jwt_methods: JWTMethods):
    resp = test_client.get("/api/v1beta/oauth2/habr", params={"user_id": "test_user"})
    assert resp.status_code == 200
    assert resp.json().get("status") == ResponseStatus.OK
    access_token = resp.json().get("access_token")
    refresh_token = resp.json().get("refresh_token")
    access_token_payload = jwt_methods.get_access_token_payload(access_token)
    refresh_token_payload = jwt_methods.get_refresh_token_payload(refresh_token)
    assert access_token_payload.user_id == "test_user"
    assert refresh_token_payload.user_id == "test_user"
