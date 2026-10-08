import os

from app import models


def test_certificate_retrieval(client, db, monkeypatch):

    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Python Workshop 2026",
            "event_date": "2026-10-08",
            "issuer": "ABC Organization",
            "recipients": [
                {
                    "name": "Anushka Salkar",
                    "email": "anushka@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    certificate = db.query(models.Certificate).filter(
        models.Certificate.job_id == job_id
    ).first()

    certificate.status = "success"
    certificate.file_path = "certificates/certificate_9999.pdf"

    db.commit()

    # Create a small temporary PDF file for the test
    os.makedirs("certificates", exist_ok=True)

    with open(
        "certificates/certificate_9999.pdf",
        "wb"
    ) as file:
        file.write(b"%PDF-1.4\nTest PDF")

    response = client.get(
        f"/api/certificates/{certificate.id}"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

    os.remove("certificates/certificate_9999.pdf")