# Bulk Certificate Generator

A REST API for generating participation certificates in bulk from a predefined certificate template.

The application accepts event details and multiple recipients, creates a background generation job, generates individual PDF certificates, tracks progress, and allows generated certificates to be downloaded.

## Features

- Create bulk certificate generation jobs
- Validate recipient email addresses
- Generate PDF certificates using ReportLab
- Process certificates independently
- One failed certificate does not stop the remaining certificates
- Track job status and generation progress
- Store job and certificate information in SQLite
- Download individual generated certificates
- Automated tests using pytest

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- HTTPX

## Project Structure

```text
Bulk-Certificate-Generator/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── certificate_generator.py
│   ├── job_processor.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_jobs.py
│       ├── test_validation.py
│       ├── test_certificate_generator.py
│       ├── test_status.py
│       ├── test_failure.py
│       └── test_retrieval.py
│
├── certificates/
├── certificates.db
├── requirements.txt
├── README.md
└── .gitignore