def test_invalid_email(client):
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Python Workshop 2026",
            "event_date": "2026-10-08",
            "issuer": "ABC Organization",
            "recipients": [
                {
                    "name": "Anushka Salkar",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422