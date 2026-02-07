#!/usr/bin/env python3
"""
One-off script to generate data/sample_merchant_summary.pdf for the take-home.
Candidates do not need to run this; the PDF is provided.
"""
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    pass


def write_minimal_pdf_no_deps(path: Path) -> None:
    """Write a minimal valid PDF with sample text (no reportlab)."""
    # Text to show - escape parens for PDF
    lines = [
        "Merchant Underwriting Summary (Sample)",
        "",
        "This document is a sample merchant terms and summary for use in the MLE take-home.",
        "Process this PDF asynchronously and extract text for the collated view or report.",
        "",
        "Section 1 - Merchant overview",
        "Merchant: Sample Merchant Ltd. Country: United Kingdom. Registration: 09446239.",
        "Monthly volume band: 50k-150k GBP.",
        "",
        "Section 2 - Key terms (abbreviated)",
        "Standard BNPL terms apply. Disputes handled per scheme rules.",
        "Chargeback liability: merchant responsible for fraud and service disputes. Settlement: T+2.",
        "",
        "Section 3 - Risk team notes",
        "Internal flag: medium. Last review 2025-01-10. No sanctions hits. Company active.",
    ]
    # Build content stream: BT /F1 12 Tf (line) Tj T* ET for each line
    stream_parts = [b"BT /F1 12 Tf 50 700 Td\n"]
    for i, line in enumerate(lines):
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_parts.append(f"({escaped}) Tj T*\n".encode("latin-1", errors="replace"))
    stream_parts.append(b"ET")
    content_stream = b"".join(stream_parts)

    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = (
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> "
        b"/Contents 4 0 R >>\nendobj\n"
    )
    obj4_header = b"4 0 obj\n<< /Length %d >>\nstream\n" % len(content_stream)
    obj4_footer = b"\nendstream\nendobj\n"
    xref_header = b"xref\n0 5\n"
    trailer = b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"

    body = b"%PDF-1.4\n" + obj1 + obj2 + obj3 + obj4_header + content_stream + obj4_footer
    xref_offset = len(body)
    # xref: 5 entries, each 20 bytes (nnnnnnnnnn ggggg n eol)
    xref_0 = b"0000000000 65535 f \n"
    xref_1 = b"%010d 00000 n \n" % (body.find(b"1 0 obj"))
    xref_2 = b"%010d 00000 n \n" % (body.find(b"2 0 obj"))
    xref_3 = b"%010d 00000 n \n" % (body.find(b"3 0 obj"))
    xref_4 = b"%010d 00000 n \n" % (body.find(b"4 0 obj"))
    body += xref_header + xref_0 + xref_1 + xref_2 + xref_3 + xref_4 + trailer % (xref_offset)
    path.write_bytes(body)

# Reportlab path
def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "sample_merchant_summary.pdf"

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    except ImportError:
        write_minimal_pdf_no_deps(path)
        print("Wrote", path, "(minimal, no reportlab)")
        return

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Merchant Underwriting Summary (Sample)", styles["Title"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            "This document is a sample merchant terms and summary for use in the MLE take-home. "
            "Process this PDF asynchronously in your pipeline and extract text for the collated view or report.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Section 1 – Merchant overview", styles["Heading2"]))
    story.append(
        Paragraph(
            "Merchant: Sample Merchant Ltd. Country: United Kingdom. Registration: 09446239. "
            "Monthly volume band: 50k–150k GBP.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Section 2 – Key terms (abbreviated)", styles["Heading2"]))
    story.append(
        Paragraph(
            "Standard BNPL terms apply. Disputes handled per scheme rules. "
            "Chargeback liability: merchant responsible for fraud and service disputes. Settlement: T+2.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Section 3 – Risk team notes", styles["Heading2"]))
    story.append(
        Paragraph(
            "Internal flag: medium. Last review 2025-01-10. No sanctions hits. Company active.",
            styles["Normal"],
        )
    )
    doc.build(story)
    print("Wrote", path)


if __name__ == "__main__":
    main()
