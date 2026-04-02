from utils.config import POST_URL


class TestLikePost:

    def test_like_post_success(self, session_b, created_post_id):
        resp = session_b.post(f"{POST_URL}/like/{created_post_id}")

        # Accept 200 (liked) or 400 (already liked if rerun)
        assert resp.status_code in [200, 400]

    def test_like_post_twice(self, session_b, created_post_id):
        session_b.post(f"{POST_URL}/like/{created_post_id}")

        resp = session_b.post(f"{POST_URL}/like/{created_post_id}")
        assert resp.status_code == 400
        assert "already liked" in resp.json()["message"]

    def test_like_nonexistent_post(self, session_a):
        fake_id = "000000000000000000000000"

        resp = session_a.post(f"{POST_URL}/like/{fake_id}")
        assert resp.status_code == 404