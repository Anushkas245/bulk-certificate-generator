from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
import os


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    issuer: str,
    certificate_id: int
):
    # Create certificates folder if it doesn't exist
    output_folder = "certificates"
    os.makedirs(output_folder, exist_ok=True)

    # PDF file path
    file_path = os.path.join(
        output_folder,
        f"certificate_{certificate_id}.pdf"
    )

    # A4 landscape
    width, height = landscape(A4)

    # Create PDF
    pdf = canvas.Canvas(file_path, pagesize=(width, height))

    # Background
    pdf.setFillColor(HexColor("#F8F5FF"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Outer border
    pdf.setStrokeColor(HexColor("#6C4AB6"))
    pdf.setLineWidth(4)
    pdf.rect(
        30,
        30,
        width - 60,
        height - 60,
        fill=0,
        stroke=1
    )

    # Inner border
    pdf.setLineWidth(1)
    pdf.rect(
        42,
        42,
        width - 84,
        height - 84,
        fill=0,
        stroke=1
    )

    # Title
    title = "CERTIFICATE OF PARTICIPATION"

    pdf.setFillColor(HexColor("#3D2A66"))
    pdf.setFont("Helvetica-Bold", 26)

    title_width = stringWidth(
        title,
        "Helvetica-Bold",
        26
    )

    pdf.drawString(
        (width - title_width) / 2,
        height - 120,
        title
    )

    # Subtitle
    pdf.setFillColor(HexColor("#555555"))
    pdf.setFont("Helvetica", 14)

    subtitle = "This certificate is proudly presented to"

    subtitle_width = stringWidth(
        subtitle,
        "Helvetica",
        14
    )

    pdf.drawString(
        (width - subtitle_width) / 2,
        height - 165,
        subtitle
    )

    # Recipient name
    pdf.setFillColor(HexColor("#6C4AB6"))
    pdf.setFont("Helvetica-Bold", 30)

    name_width = stringWidth(
        recipient_name,
        "Helvetica-Bold",
        30
    )

    pdf.drawString(
        (width - name_width) / 2,
        height - 225,
        recipient_name
    )

    # Participation text
    pdf.setFillColor(HexColor("#555555"))
    pdf.setFont("Helvetica", 14)

    text = "for successfully participating in"

    text_width = stringWidth(
        text,
        "Helvetica",
        14
    )

    pdf.drawString(
        (width - text_width) / 2,
        height - 265,
        text
    )

    # Event name
    pdf.setFillColor(HexColor("#3D2A66"))
    pdf.setFont("Helvetica-Bold", 20)

    event_width = stringWidth(
        event_name,
        "Helvetica-Bold",
        20
    )

    pdf.drawString(
        (width - event_width) / 2,
        height - 305,
        event_name
    )

    # Date
    pdf.setFillColor(HexColor("#555555"))
    pdf.setFont("Helvetica", 13)

    date_text = f"Date: {event_date}"

    date_width = stringWidth(
        date_text,
        "Helvetica",
        13
    )

    pdf.drawString(
        (width - date_width) / 2,
        100,
        date_text
    )

    # Issuer
    pdf.setFont("Helvetica-Bold", 14)

    issuer_width = stringWidth(
        issuer,
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        (width - issuer_width) / 2,
        75,
        issuer
    )

    # Finish PDF
    pdf.save()

    return file_path

