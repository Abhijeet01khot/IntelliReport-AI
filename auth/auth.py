import hashlib
import secrets

from database.database import (
    init_db,
    create_user,
    get_user_by_email,
)


# Number of PBKDF2 iterations used for password hashing.
PBKDF2_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.

    A random salt is generated for every password.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    return (
        f"pbkdf2_sha256$"
        f"{PBKDF2_ITERATIONS}$"
        f"{salt.hex()}$"
        f"{password_hash.hex()}"
    )


def verify_password(
    password: str,
    stored_value: str
) -> bool:
    """
    Verify a password against its stored PBKDF2 hash.
    """

    try:
        algorithm, iterations, salt_hex, hash_hex = (
            stored_value.split("$")
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return secrets.compare_digest(
            actual_hash,
            expected_hash
        )

    except (ValueError, TypeError):
        return False


def register_user(
    name: str,
    email: str,
    password: str
) -> tuple[bool, str]:
    """
    Register a new user.

    Returns:
        (True, success message)
        (False, error message)
    """

    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Name is required."

    if not email:
        return False, "Email is required."

    if not password:
        return False, "Password is required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    # Make sure the database/tables exist.
    init_db()

    # Check whether email already exists.
    existing_user = get_user_by_email(email)

    if existing_user is not None:
        return False, "An account with this email already exists."

    # Hash password before storing it.
    password_hash = hash_password(password)

    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    if user_id is None:
        return False, "An account with this email already exists."

    return True, "Account created successfully."


def authenticate_user(
    email: str,
    password: str
):
    """
    Authenticate a user using email and password.

    Returns:
        User dictionary if credentials are valid.
        None otherwise.
    """

    email = email.strip().lower()

    if not email or not password:
        return None

    init_db()

    user = get_user_by_email(email)

    if user is None:
        return None

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    return user