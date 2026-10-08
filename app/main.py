from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from . import models
from .schemas import JobCreate
from .job_processor import process_job


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for generating certificates in bulk",
    version="1.0.0"
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


# ---------------------------------------------------------
# CREATE BULK CERTIFICATE GENERATION JOB
# ---------------------------------------------------------

@app.post("/api/jobs")
def create_job(
    job: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create the main job
    new_job = models.Job(
        event_name=job.event_name,
        event_date=str(job.event_date),
        issuer=job.issuer,
        total=len(job.recipients),
        status="pending"
    )

    db.add(new_job)

    # Get generated Job ID
    db.flush()

    # Create a certificate record for every recipient
    for recipient in job.recipients:
        certificate = models.Certificate(
            job_id=new_job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="pending"
        )

        db.add(certificate)

    # Save job and certificate records
    db.commit()
    db.refresh(new_job)

    # Start certificate generation in background
    background_tasks.add_task(
        process_job,
        new_job.id
    )

    return {
        "job_id": new_job.id,
        "status": "processing",
        "total": new_job.total
    }


# ---------------------------------------------------------
# GET JOB STATUS
# ---------------------------------------------------------

@app.get("/api/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    # Find job
    job = db.query(models.Job).filter(
        models.Job.id == job_id
    ).first()

    # Job not found
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Calculate processed certificates
    processed = job.successful + job.failed

    # Calculate progress
    if job.total > 0:
        progress = (processed / job.total) * 100
    else:
        progress = 0

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "issuer": job.issuer,

        "status": job.status,

        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
        "processed": processed,

        "progress": round(progress, 2),

        "certificates": [
            {
                "id": certificate.id,
                "name": certificate.recipient_name,
                "email": certificate.recipient_email,
                "status": certificate.status,
                "file_path": certificate.file_path,
                "error": certificate.error_message
            }
            for certificate in job.certificates
        ]
    }


# ---------------------------------------------------------
# DOWNLOAD GENERATED CERTIFICATE
# ---------------------------------------------------------

@app.get("/api/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    # Find certificate
    certificate = db.query(models.Certificate).filter(
        models.Certificate.id == certificate_id
    ).first()

    # Certificate not found
    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    # Certificate generation failed or is still pending
    if certificate.status != "success":
        raise HTTPException(
            status_code=400,
            detail="Certificate has not been generated successfully"
        )

    # File path missing
    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    # Return PDF
    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )