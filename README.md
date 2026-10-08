# Bulk Certificate Generator API

A REST API built with **FastAPI** for generating participation certificates in bulk from a predefined certificate template.

The application accepts event details and multiple recipients, creates a generation job, processes certificates in the background, tracks job progress, handles individual failures without stopping the complete job, and provides an API to download generated certificates.

---

## Features

- Create bulk certificate generation jobs
- Validate recipient email addresses
- Generate individual PDF certificates
- Background certificate processing
- Track job status and progress
- Handle individual certificate failures independently
- Store job and certificate information in SQLite
- Download generated certificates through an API
- Interactive Swagger API documentation
- Automated tests using pytest

---

## Tech Stack

- **Python**
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM and database management
- **SQLite** – Relational database
- **Pydantic** – Request validation
- **ReportLab** – PDF certificate generation
- **Pytest** – Automated testing
- **HTTPX** – API testing

---

## How It Works

```text
Client
   |
   | POST /api/jobs
   v
FastAPI API
   |
   |-- Validate Request
   |
   |-- Create Job
   |
   |-- Store Recipients
   |
   |-- Start Background Task
   |
   v
Job Processor
   |
   |-- Recipient 1 --> Generate PDF --> Success
   |
   |-- Recipient 2 --> Generate PDF --> Success
   |
   |-- Recipient 3 --> Generate PDF --> Failed
   |
   v
Database
   |
   |-- Job Status
   |-- Progress
   |-- Success Count
   |-- Failure Count
   |
   v
Certificate Download API
