import requests
from utils.config import AUTH_URL
from tests.test_data import USER_A
from utils.helpers import unique_user


class TestRegister:

    def test_register_new_user_success(self):
        unique = unique_user("newuser")
        resp = requests.post(f"{AUTH_URL}/register", json=unique)

        assert resp.status_code == 201
        data = resp.json()
        assert "user" in data
        assert data["user"]["username"] == unique["username"]

    def test_register_duplicate_username(self):
        # Ensure base user exists first
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        payload = {
            "username": USER_A["username"],
            "email": "different_email@test.com",
            "password": "Test@1234"
        }

        resp = requests.post(f"{AUTH_URL}/register", json=payload)
        assert resp.status_code == 400
        assert "Username already exists" in resp.json()["message"]

    def test_register_duplicate_email(self):
            base_user = unique_user("emailbase")
            requests.post(f"{AUTH_URL}/register", json=base_user)

            payload = {
                    "username": f"fresh_{base_user['username']}",
                    "email": base_user["email"],
                    "password": "Test@1234"
    }

            resp = requests.post(f"{AUTH_URL}/register", json=payload)
            assert resp.status_code == 400
            assert "Email already exists" in resp.json()["message"]

    def test_register_response_does_not_expose_password(self):
        unique = unique_user("sectest")
        unique["password"] = "Secret@Pass"

        resp = requests.post(f"{AUTH_URL}/register", json=unique)
        assert "password" not in resp.json().get("user", {})

    def test_register_sets_cookie(self):
        unique = unique_user("cookietest")
        unique["password"] = "Test@Cookie"

        resp = requests.post(f"{AUTH_URL}/register", json=unique)
        assert resp.status_code == 201
        assert "token" in resp.cookies


class TestLogin:

    def test_login_with_username_success(self):
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": USER_A["username"],
            "password": USER_A["password"]
        })

        assert resp.status_code == 200
        assert resp.json()["user"]["username"] == USER_A["username"]

    def test_login_with_email_success(self):
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        resp = requests.post(f"{AUTH_URL}/login", json={
            "email": USER_A["email"],
            "password": USER_A["password"]
        })

        assert resp.status_code == 200

    def test_login_wrong_password(self):
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": USER_A["username"],
            "password": "WrongPassword123"
        })

        assert resp.status_code == 400

    def test_login_nonexistent_user(self):
        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": "ghost_user_xyz_999",
            "password": "SomePass@123"
        })

        assert resp.status_code == 404

    def test_login_sets_cookie(self):
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": USER_A["username"],
            "password": USER_A["password"]
        })

        assert "token" in resp.cookies

    def test_login_response_does_not_expose_password(self):
        requests.post(f"{AUTH_URL}/register", json=USER_A)

        resp = requests.post(f"{AUTH_URL}/login", json={
            "username": USER_A["username"],
            "password": USER_A["password"]
        })

        assert "password" not in resp.json().get("user", {})