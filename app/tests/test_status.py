def test_job_status_and_progress(client, db):
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
                },
                {
                    "name": "Rahul Sharma",
                    "email": "rahul@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total"] == 2
    assert "successful" in data
    assert "failed" in data
    assert "processed" in data
    assert "progress" in data
    assert "certificates" in data

    assert 0 <= data["progress"] <= 100