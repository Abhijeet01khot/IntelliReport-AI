from auth.auth import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
)


def test_password_hashing():
    password = "MySecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)


def test_password_hashes_are_different():
    password = "MySecurePassword123!"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_register_user():
    success, message = register_user(
        "Auth Test User",
        "auth_test@example.com",
        "Password123!"
    )

    assert success is True
    assert "success" in message.lower()


def test_duplicate_email():
    email = "duplicate_test@example.com"

    first_success, _ = register_user(
        "First User",
        email,
        "Password123!"
    )

    second_success, second_message = register_user(
        "Second User",
        email,
        "Password456!"
    )

    assert first_success is True
    assert second_success is False
    assert "already" in second_message.lower()


def test_authenticate_user():
    email = "login_test@example.com"
    password = "LoginPassword123!"

    success, _ = register_user(
        "Login Test User",
        email,
        password
    )

    assert success is True

    user = authenticate_user(
        email,
        password
    )

    assert user is not None
    assert user["email"] == email
    assert user["name"] == "Login Test User"


def test_wrong_password():
    email = "wrong_password@example.com"

    register_user(
        "Wrong Password User",
        email,
        "CorrectPassword123!"
    )

    user = authenticate_user(
        email,
        "WrongPassword123!"
    )

    assert user is None


if __name__ == "__main__":
    test_password_hashing()
    test_password_hashes_are_different()
    test_register_user()
    test_duplicate_email()
    test_authenticate_user()
    test_wrong_password()

    print("Authentication tests passed successfully!")