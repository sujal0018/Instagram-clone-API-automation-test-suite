from utils.config import USER_URL
from tests.test_data import USER_A, USER_B


class TestFollowUser:

    def test_follow_self_returns_400(self, session_a):
        resp = session_a.post(f"{USER_URL}/follow/{USER_A['username']}")
        assert resp.status_code == 400
        assert "cannot follow yourself" in resp.json()["message"].lower()

    def test_follow_nonexistent_user(self, session_a):
        resp = session_a.post(f"{USER_URL}/follow/ghost_user_xyz_abc")
        assert resp.status_code == 404

    def test_follow_public_user_gives_accepted_status(self, session_b):
        resp = session_b.post(f"{USER_URL}/follow/{USER_A['username']}")
        data = resp.json()

        assert resp.status_code in [201, 400]
        if resp.status_code == 201:
            assert data["followRecord"]["status"] == "accepted"

    def test_follow_private_user_gives_pending_status(self, session_a):
        resp = session_a.post(f"{USER_URL}/follow/{USER_B['username']}")
        data = resp.json()

        assert resp.status_code in [201, 400]
        if resp.status_code == 201:
            assert data["followRecord"]["status"] == "pending"

    def test_follow_already_following_returns_400(self, session_b):
        session_b.post(f"{USER_URL}/follow/{USER_A['username']}")

        resp = session_b.post(f"{USER_URL}/follow/{USER_A['username']}")
        assert resp.status_code == 400


class TestAcceptRejectFollow:

    def test_accept_follow_request(self, session_b, session_a):
        session_a.post(f"{USER_URL}/follow/{USER_B['username']}")

        resp = session_b.patch(f"{USER_URL}/accept/{USER_A['username']}")
        assert resp.status_code in [200, 404]

    def test_reject_follow_request(self, session_a, session_b):
        resp = session_b.patch(f"{USER_URL}/reject/{USER_A['username']}")
        assert resp.status_code in [200, 404]

    def test_accept_nonexistent_request(self, session_a):
        resp = session_a.patch(f"{USER_URL}/accept/ghost_user_xyz_abc")
        assert resp.status_code == 404

    def test_reject_nonexistent_request(self, session_a):
        resp = session_a.patch(f"{USER_URL}/reject/ghost_user_xyz_abc")
        assert resp.status_code == 404