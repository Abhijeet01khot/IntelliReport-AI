from database.database import (
    init_db,
    create_user,
    get_user_by_email,
    save_report,
    get_reports_by_user,
    get_report_by_id,
    get_user_report_stats,
)


def test_database():
    init_db()

    email = "test@example.com"

    # Create user
    user_id = create_user(
        "Test User",
        email,
        "test_password_hash"
    )

    # If test was previously run, retrieve existing user
    if user_id is None:
        user = get_user_by_email(email)
        user_id = user["id"]

    # Check user
    user = get_user_by_email(email)

    assert user is not None
    assert user["email"] == email

    # Save report
    report_id = save_report(
        user_id=user_id,
        topic="Artificial Intelligence",
        report="This is a test AI report.",
        review="Test review.",
        execution_time=5.25,
        word_count=6
    )

    assert report_id is not None

    # Get reports
    reports = get_reports_by_user(user_id)

    assert len(reports) >= 1

    # Get specific report
    report = get_report_by_id(
        user_id,
        report_id
    )

    assert report is not None
    assert report["topic"] == "Artificial Intelligence"

    # Check statistics
    stats = get_user_report_stats(user_id)

    assert stats["report_count"] >= 1
    assert stats["total_words"] >= 6


if __name__ == "__main__":
    test_database()
    print("Database test passed successfully!")