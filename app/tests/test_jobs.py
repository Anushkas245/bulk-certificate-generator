def test_create_generation_job(client):
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

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "processing"
    assert data["total"] == 2