import pytest
import requests
from utils.config import AUTH_URL, POST_URL
from tests.test_data import USER_A, USER_B


@pytest.fixture(scope="session")
def session_a():
    session = requests.Session()

    # Try register (ignore if already exists)
    session.post(f"{AUTH_URL}/register", json=USER_A)

    # Login
    resp = session.post(f"{AUTH_URL}/login", json={
        "username": USER_A["username"],
        "password": USER_A["password"]
    })

    assert resp.status_code == 200, f"USER_A login failed: {resp.text}"
    return session


@pytest.fixture(scope="session")
def session_b():
    session = requests.Session()

    session.post(f"{AUTH_URL}/register", json=USER_B)

    resp = session.post(f"{AUTH_URL}/login", json={
        "username": USER_B["username"],
        "password": USER_B["password"]
    })

    assert resp.status_code == 200, f"USER_B login failed: {resp.text}"
    return session


@pytest.fixture(scope="session")
def created_post_id(session_a):
    with open("test_assets/test_image.jpg", "rb") as f:
        resp = session_a.post(
            f"{POST_URL}/create",
            data={"caption": "Test post for QA suite"},
            files={"image": ("test_image.jpg", f, "image/jpeg")}
        )

    assert resp.status_code == 201, f"Post creation failed: {resp.text}"
    return resp.json()["post"]["_id"]