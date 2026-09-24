import sqlite3
from pathlib import Path
from typing import Optional


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database directory and file
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "intellireport.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db() -> None:
    """
    Create all required database tables if they do not already exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Reports table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                report TEXT NOT NULL,
                review TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_time REAL DEFAULT 0,
                word_count INTEGER DEFAULT 0,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def create_user(
    name: str,
    email: str,
    password_hash: str
) -> Optional[int]:
    """
    Create a new user.

    Returns:
        User ID if successful.
        None if email already exists.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                password_hash
            )
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        connection.close()


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Retrieve a user using their email address.

    Returns:
        Dictionary containing user information,
        or None if user does not exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                created_at
            FROM users
            WHERE email = ?
            """,
            (email.strip().lower(),)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def save_report(
    user_id: int,
    topic: str,
    report: str,
    review: str,
    execution_time: float,
    word_count: int
) -> int:
    """
    Save a generated report for a specific user.

    Returns:
        Newly created report ID.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO reports (
                user_id,
                topic,
                report,
                review,
                execution_time,
                word_count
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                topic.strip(),
                report,
                review,
                execution_time,
                word_count
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_reports_by_user(user_id: int) -> list[dict]:
    """
    Retrieve all reports belonging to a specific user.

    Newest reports are returned first.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                topic,
                report,
                review,
                created_at,
                execution_time,
                word_count
            FROM reports
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_report_by_id(
    user_id: int,
    report_id: int
) -> Optional[dict]:
    """
    Retrieve one report.

    IMPORTANT:
    The user_id is checked as well, so a user cannot
    access another user's report.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                topic,
                report,
                review,
                created_at,
                execution_time,
                word_count
            FROM reports
            WHERE id = ?
              AND user_id = ?
            """,
            (
                report_id,
                user_id
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def get_user_report_stats(user_id: int) -> dict:
    """
    Return report statistics for a specific user.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*) AS report_count,
                COALESCE(SUM(word_count), 0) AS total_words,
                COALESCE(AVG(execution_time), 0) AS average_execution_time
            FROM reports
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        return {
            "report_count": row["report_count"],
            "total_words": row["total_words"],
            "average_execution_time": row["average_execution_time"],
        }

    finally:
        connection.close()