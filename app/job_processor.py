from datetime import datetime, timezone
from .database import SessionLocal
from .models import Job, Certificate
from .certificate_generator import generate_certificate


def process_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        certificates = db.query(Certificate).filter(
            Certificate.job_id == job_id
        ).all()

        for certificate in certificates:

            try:
                file_path = generate_certificate(
                    recipient_name=certificate.recipient_name,
                    event_name=job.event_name,
                    event_date=job.event_date,
                    issuer=job.issuer,
                    certificate_id=certificate.id
                )

                certificate.status = "success"
                certificate.file_path = file_path

                job.successful += 1

            except Exception as e:
                certificate.status = "failed"
                certificate.error_message = str(e)

                job.failed += 1

            db.commit()

        job.status = "completed"
        job.completed_at = datetime.now(timezone.utc)
        db.commit()

    finally:
        db.close()