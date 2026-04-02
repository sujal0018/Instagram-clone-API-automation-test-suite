import requests
from utils.config import AUTH_URL, POST_URL
from tests.test_data import USER_A


class TestResponseTimes:

    def test_login_response_time(self):
        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": USER_A["username"],
            "password": USER_A["password"]
        })

        assert resp.elapsed.total_seconds() < 3.0

    def test_get_all_posts_response_time(self, session_a):
        resp = session_a.get(f"{POST_URL}/getallposts")
        assert resp.elapsed.total_seconds() < 3.0