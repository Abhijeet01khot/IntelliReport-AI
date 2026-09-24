from auth.auth import hash_password, verify_password


def test_authentication_password_flow():
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password(
        "WrongPassword123!",
        hashed
    )


if __name__ == "__main__":
    test_authentication_password_flow()
    print("Authentication UI dependency test passed!")