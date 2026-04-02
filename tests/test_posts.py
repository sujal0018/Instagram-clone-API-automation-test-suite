import requests
from utils.config import POST_URL


class TestCreatePost:

    def test_create_post_success(self, session_a):
        with open("test_assets/test_image.jpg", "rb") as f:
            resp = session_a.post(
                f"{POST_URL}/create",
                data={"caption": "Hello from pytest!"},
                files={"image": ("test_image.jpg", f, "image/jpeg")}
            )

        assert resp.status_code == 201
        data = resp.json()
        assert "post" in data
        assert data["post"]["caption"] == "Hello from pytest!"

    def test_create_post_unauthenticated(self):
        with open("test_assets/test_image.jpg", "rb") as f:
            resp = requests.post(
                f"{POST_URL}/create",
                data={"caption": "No auth test"},
                files={"image": ("test_image.jpg", f, "image/jpeg")}
            )

        assert resp.status_code == 401


class TestGetPosts:

    def test_get_all_posts_success(self, session_a):
        resp = session_a.get(f"{POST_URL}/getallposts")
        assert resp.status_code == 200

        data = resp.json()
        assert "posts" in data
        assert isinstance(data["posts"], list)

    def test_get_all_posts_unauthenticated(self):
        resp = requests.get(f"{POST_URL}/getallposts")
        assert resp.status_code == 401

    def test_get_single_post_success(self, session_a, created_post_id):
        resp = session_a.get(f"{POST_URL}/getuserposts/{created_post_id}")
        assert resp.status_code == 200
        assert resp.json()["post"]["_id"] == created_post_id

    def test_get_post_invalid_id(self, session_a):
        resp = session_a.get(f"{POST_URL}/getuserposts/notavalidid")
        assert resp.status_code in [400, 404, 500]

    def test_get_post_wrong_owner(self, session_b, created_post_id):
        resp = session_b.get(f"{POST_URL}/getuserposts/{created_post_id}")
        assert resp.status_code == 403
        assert "Unauthorized" in resp.json()["message"]


class TestDeletePost:

    def test_delete_post_wrong_owner(self, session_b, created_post_id):
        resp = session_b.delete(f"{POST_URL}/deletepost/{created_post_id}")
        assert resp.status_code == 403

    def test_delete_post_success(self, session_a):
        with open("test_assets/test_image.jpg", "rb") as f:
            create_resp = session_a.post(
                f"{POST_URL}/create",
                data={"caption": "Post to be deleted"},
                files={"image": ("test_image.jpg", f, "image/jpeg")}
            )

        post_id = create_resp.json()["post"]["_id"]

        resp = session_a.delete(f"{POST_URL}/deletepost/{post_id}")
        assert resp.status_code == 200
        assert "deleted successfully" in resp.json()["message"]

    def test_delete_already_deleted_post(self, session_a):
        fake_mongo_id = "000000000000000000000000"
        resp = session_a.delete(f"{POST_URL}/deletepost/{fake_mongo_id}")
        assert resp.status_code == 404