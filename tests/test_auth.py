import uuid

from auth.auth import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
)


def unique_email(prefix):
    return f"{prefix}_{uuid.uuid4().hex}@example.com"


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
    email = unique_email("auth_test")

    success, message = register_user(
        "Auth Test User",
        email,
        "Password123!"
    )

    assert success is True, message
    assert "success" in message.lower()


def test_duplicate_email():
    email = unique_email("duplicate_test")

    first_success, first_message = register_user(
        "First User",
        email,
        "Password123!"
    )

    second_success, second_message = register_user(
        "Second User",
        email,
        "Password456!"
    )

    assert first_success is True, first_message
    assert second_success is False
    assert "already" in second_message.lower()


def test_authenticate_user():
    email = unique_email("login_test")
    password = "LoginPassword123!"

    success, message = register_user(
        "Login Test User",
        email,
        password
    )

    assert success is True, message

    user = authenticate_user(
        email,
        password
    )

    assert user is not None
    assert user["email"] == email
    assert user["name"] == "Login Test User"


def test_wrong_password():
    email = unique_email("wrong_password")

    success, message = register_user(
        "Wrong Password User",
        email,
        "CorrectPassword123!"
    )

    assert success is True, message

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