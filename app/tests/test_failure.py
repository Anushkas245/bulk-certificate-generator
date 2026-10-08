from sqlalchemy.orm import sessionmaker

from app.job_processor import process_job
from app import models


def test_one_recipient_failure_does_not_stop_job(
    client,
    db,
    monkeypatch
):
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Python Workshop 2026",
            "event_date": "2026-10-08",
            "issuer": "ABC Organization",
            "recipients": [
                {
                    "name": "Good User",
                    "email": "good@example.com"
                },
                {
                    "name": "Bad User",
                    "email": "bad@example.com"
                },
                {
                    "name": "Another Good User",
                    "email": "good2@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    def fake_generate_certificate(
        recipient_name,
        event_name,
        event_date,
        issuer,
        certificate_id
    ):
        if recipient_name == "Bad User":
            raise Exception("Test generation failure")

        return f"certificates/test_{certificate_id}.pdf"

    monkeypatch.setattr(
        "app.job_processor.generate_certificate",
        fake_generate_certificate
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db.bind
    )

    monkeypatch.setattr(
        "app.job_processor.SessionLocal",
        TestSessionLocal
    )

    process_job(job_id)

    db.expire_all()

    job = db.query(models.Job).filter(
        models.Job.id == job_id
    ).first()

    certificates = db.query(models.Certificate).filter(
        models.Certificate.job_id == job_id
    ).order_by(models.Certificate.id).all()

    assert job.status == "completed"
    assert job.total == 3
    assert job.successful == 2
    assert job.failed == 1

    assert certificates[0].status == "success"
    assert certificates[1].status == "failed"
    assert certificates[2].status == "success"

    assert certificates[1].error_message == "Test generation failure"