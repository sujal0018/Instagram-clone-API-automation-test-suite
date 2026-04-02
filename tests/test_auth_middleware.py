import requests
from utils.config import POST_URL


class TestAuthMiddleware:

    def test_protected_route_without_cookie_returns_401(self):
        resp = requests.get(f"{POST_URL}/getallposts")
        assert resp.status_code == 401

    def test_protected_route_with_invalid_token_returns_401(self):
        session = requests.Session()
        session.cookies.set("token", "this.is.a.fake.jwt.token")

        resp = session.get(f"{POST_URL}/getallposts")
        assert resp.status_code == 401