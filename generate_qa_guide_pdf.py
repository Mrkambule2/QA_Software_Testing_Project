import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def build_qa_guide_pdf(filename="Software_Testing_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#002855")  # Navy
    secondary_color = colors.HexColor("#FFB800") # Gold
    dark_gray = colors.HexColor("#2C3E50")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=0,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=dark_gray,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=dark_gray,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1A252C"),
        backColor=colors.HexColor("#F0F4F8"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("Software Quality Assurance & Testing Guide", title_style))
    story.append(Paragraph("Standard Operating Procedure for Test Execution & Developer Reporting", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary_color, spaceBefore=0, spaceAfter=15))

    # Section 1: Overview
    story.append(Paragraph("1. Overview of Software Testing Methodologies", h1_style))
    story.append(Paragraph(
        "Software testing ensures that application features work reliably, perform standard error handling, and meet specified requirements. Standard testing methodologies include:",
        body_style
    ))
    story.append(Paragraph("• <b>Unit Testing:</b> Verifies individual functions, classes, and business logic components in isolation.", bullet_style))
    story.append(Paragraph("• <b>Integration & API Testing:</b> Ensures microservices, APIs, and databases communicate as expected.", bullet_style))
    story.append(Paragraph("• <b>Functional & UI Testing:</b> Validates complete user workflows, screen widgets, and interactive behaviors.", bullet_style))
    story.append(Paragraph("• <b>Performance Testing:</b> Benchmarks response latency and stability under expected system load.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 2: Prerequisites
    story.append(Paragraph("2. Prerequisites & Environment Setup", h1_style))
    story.append(Paragraph(
        "Before executing test automation scripts, ensure your local environment has the required runtime environments installed:",
        body_style
    ))

    setup_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Requirement / Command</b>", body_style), Paragraph("<b>Purpose</b>", body_style)],
        [Paragraph("Python 3.x", body_style), Paragraph("<code>python --version</code>", body_style), Paragraph("Executes Python API & Functional test suites", body_style)],
        [Paragraph("ReportLab", body_style), Paragraph("<code>pip install reportlab</code>", body_style), Paragraph("Generates automated PDF test reports", body_style)],
        [Paragraph("Requests", body_style), Paragraph("<code>pip install requests</code>", body_style), Paragraph("Handles HTTP API testing requests", body_style)],
    ]

    t = Table(setup_data, colWidths=[100, 160, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    story.append(Spacer(1, 12))

    # Section 3: Executing Test Scripts
    story.append(Paragraph("3. Step-by-Step Test Execution Commands", h1_style))

    story.append(Paragraph("A. Running Automated Python Test Suite", h2_style))
    story.append(Paragraph("Execute the Python test suite from your terminal or command prompt:", body_style))
    story.append(Paragraph("python test_suite.py", code_style))
    story.append(Paragraph(
        "This command runs all test cases (Status code checks, Schema validation, Bad input handling, and Latency benchmarks) "
        "and automatically outputs a summary PDF named <b>test_report.pdf</b>.",
        body_style
    ))

    story.append(Paragraph("B. Running Master Test Runner", h2_style))
    story.append(Paragraph("Execute all tests and generate all PDF documentation at once:", body_style))
    story.append(Paragraph("python run_all_qa_tests.py", code_style))

    story.append(Spacer(1, 10))

    # Section 4: Analyzing Test Output & PDF Reports
    story.append(Paragraph("4. Analyzing Test Output & PDF Reports", h1_style))
    story.append(Paragraph(
        "When the automated test script finishes, it generates execution metrics. Review the output as follows:",
        body_style
    ))
    story.append(Paragraph("• <b>PASS:</b> The feature behaves according to specifications.", bullet_style))
    story.append(Paragraph("• <b>FAIL:</b> The test assertion failed (e.g., unexpected status code or missing field).", bullet_style))
    story.append(Paragraph("• <b>ERROR:</b> An unhandled exception or connection error occurred during execution.", bullet_style))
    story.append(Paragraph("• <b>PDF Summary:</b> Open <code>test_report.pdf</code> to view execution timestamps, pass rates, and logs.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 5: Developer Bug Reporting Protocol
    story.append(Paragraph("5. Submitting Bug Reports to Development Teams", h1_style))
    story.append(Paragraph(
        "When a test fails, submit a structured bug report to the development team with the following details:",
        body_style
    ))

    bug_report_data = [
        [Paragraph("<b>Field</b>", body_style), Paragraph("<b>Description & Example</b>", body_style)],
        [Paragraph("Title", body_style), Paragraph("Concise summary (e.g., <i>[API] /users endpoint returns 500 on valid POST request</i>)", body_style)],
        [Paragraph("Severity", body_style), Paragraph("Critical (Blocker), High (Major feature broken), Medium, or Low", body_style)],
        [Paragraph("Steps to Reproduce", body_style), Paragraph("1. Run <code>python test_suite.py</code><br/>2. Observe failure in <code>test_invalid_input_handling</code>", body_style)],
        [Paragraph("Expected Behavior", body_style), Paragraph("API should return HTTP 400 Bad Request with validation error message", body_style)],
        [Paragraph("Actual Behavior", body_style), Paragraph("API returns HTTP 500 Internal Server Error without body details", body_style)],
        [Paragraph("Attachments", body_style), Paragraph("Attach <code>test_report.pdf</code> and relevant console stack traces", body_style)]
    ]

    t_bug = Table(bug_report_data, colWidths=[130, 390])
    t_bug.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_bug)

    guide_path = os.path.join(os.path.dirname(__file__), filename)
    doc.build(story)
    print(f"[SUCCESS] PDF Guide generated: {os.path.abspath(guide_path)}")

if __name__ == '__main__':
    build_qa_guide_pdf()
