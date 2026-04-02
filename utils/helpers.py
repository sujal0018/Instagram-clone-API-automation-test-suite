import time

def unique_user(prefix="testuser"):
    timestamp = int(time.time())
    return {
        "username": f"{prefix}_{timestamp}",
        "email": f"{prefix}_{timestamp}@test.com",
        "password": "Test@1234"
    }