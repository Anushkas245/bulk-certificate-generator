from app.certificate_generator import generate_certificate
import os


def test_certificate_generation():
    file_path = generate_certificate(
        recipient_name="Test User",
        event_name="Python Workshop 2026",
        event_date="2026-10-08",
        issuer="ABC Organization",
        certificate_id=9999
    )

    assert os.path.exists(file_path)
    assert file_path.endswith(".pdf")

    os.remove(file_path)