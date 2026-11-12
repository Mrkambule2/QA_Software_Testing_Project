import unittest
import time
import datetime
import os
import sys
import requests

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

# Global variable for target URL
TARGET_URL = "https://httpbin.org"

class WebsiteQATestSuite(unittest.TestCase):
    """
    Automated QA Test Suite for Web Software & APIs.
    Tests reachability, headers, latency, 404 handling, and content types.
    """

    def test_1_website_reachability(self):
        """Verify target website/service is online and returns HTTP 200 OK."""
        try:
            response = requests.get(TARGET_URL, timeout=10)
            self.assertIn(response.status_code, [200, 301, 302], f"HTTP status code was {response.status_code}")
        except Exception as e:
            self.fail(f"Failed to connect to target {TARGET_URL}: {e}")

    def test_2_response_headers_check(self):
        """Verify target website includes standard HTTP headers."""
        try:
            response = requests.get(TARGET_URL, timeout=10)
            self.assertIn("Content-Type", response.headers, "Response missing Content-Type header")
        except Exception as e:
            self.fail(f"Header check error on {TARGET_URL}: {e}")

    def test_3_response_latency_benchmark(self):
        """Benchmark HTTP response time (must respond within 3000ms)."""
        try:
            start_time = time.time()
            response = requests.get(TARGET_URL, timeout=10)
            elapsed_ms = (time.time() - start_time) * 1000
            self.assertLess(elapsed_ms, 3000, f"Response latency {elapsed_ms:.2f}ms exceeded limit")
        except Exception as e:
            self.fail(f"Latency check error on {TARGET_URL}: {e}")

    def test_4_invalid_endpoint_404_handling(self):
        """Verify target website handles invalid endpoints with HTTP 404."""
        try:
            invalid_url = f"{TARGET_URL.rstrip('/')}/non_existent_qa_test_page_98765"
            response = requests.get(invalid_url, timeout=10)
            self.assertEqual(response.status_code, 404, f"Expected 404 Not Found, got {response.status_code}")
        except Exception as e:
            self.fail(f"404 handling check error on {invalid_url}: {e}")

    def test_5_content_type_validation(self):
        """Verify target returns valid text or JSON content."""
        try:
            response = requests.get(TARGET_URL, timeout=10)
            content_type = response.headers.get("Content-Type", "")
            is_valid_type = any(t in content_type for t in ["text/html", "application/json", "text/plain"])
            self.assertTrue(is_valid_type, f"Unexpected Content-Type: {content_type}")
        except Exception as e:
            self.fail(f"Content type validation error on {TARGET_URL}: {e}")


class DetailedTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        doc_text = test._testMethodDoc.strip() if test._testMethodDoc else "No description"
        self.test_records.append({
            "name": test._testMethodName,
            "doc": doc_text,
            "status": "PASS"
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        doc_text = test._testMethodDoc.strip() if test._testMethodDoc else "No description"
        self.test_records.append({
            "name": test._testMethodName,
            "doc": doc_text,
            "status": "FAIL"
        })

    def addError(self, test, err):
        super().addError(test, err)
        doc_text = test._testMethodDoc.strip() if test._testMethodDoc else "No description"
        self.test_records.append({
            "name": test._testMethodName,
            "doc": doc_text,
            "status": "ERROR"
        })


def generate_pdf_test_report(results_data, target_url, filename="test_report.pdf"):
    """Generates a professional PDF Test Execution Report."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#002855")
    secondary_color = colors.HexColor("#FFB800")

    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Automated Software Test Execution Report", title_style))
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Target Website/API:</b> {target_url}<br/><b>Execution Date:</b> {now_str}", meta_style))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary_color, spaceBefore=0, spaceAfter=15))

    # Summary Stats Table
    passed_count = results_data["passed"]
    failed_count = results_data["failed"]
    total_count = results_data["total"]
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0

    summary_data = [
        [Paragraph("<b>Total Tests</b>", body_style), Paragraph("<b>Passed</b>", body_style), Paragraph("<b>Failed</b>", body_style), Paragraph("<b>Pass Rate</b>", body_style)],
        [Paragraph(str(total_count), body_style), Paragraph(f"<font color='green'><b>{passed_count}</b></font>", body_style), Paragraph(f"<font color='red'><b>{failed_count}</b></font>", body_style), Paragraph(f"<b>{pass_rate:.1f}%</b>", body_style)]
    ]

    summary_table = Table(summary_data, colWidths=[130, 130, 130, 150])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # Detailed Results
    story.append(Paragraph("Test Case Details", h2_style))

    details_data = [
        [Paragraph("<b>Test Case Name</b>", body_style), Paragraph("<b>Description</b>", body_style), Paragraph("<b>Result</b>", body_style)]
    ]

    for item in results_data["details"]:
        status_color = "green" if item["status"] == "PASS" else "red"
        details_data.append([
            Paragraph(item["name"], body_style),
            Paragraph(item["doc"], body_style),
            Paragraph(f"<font color='{status_color}'><b>{item['status']}</b></font>", body_style)
        ])

    details_table = Table(details_data, colWidths=[180, 260, 100])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(details_table)

    doc.build(story)
    print(f"[SUCCESS] Test Execution PDF Report generated: {os.path.abspath(filename)}")


def run_tests_and_report():
    global TARGET_URL

    # Check if URL was passed via command line argument or prompt
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        TARGET_URL = sys.argv[1]
    else:
        # Prompt user if running interactively
        user_input = input("Enter Website / API URL to test (Press Enter for 'https://httpbin.org'): ").strip()
        if user_input:
            if not user_input.startswith("http://") and not user_input.startswith("https://"):
                TARGET_URL = "https://" + user_input
            else:
                TARGET_URL = user_input

    print(f"\n[INFO] Starting QA Software Test Suite against: {TARGET_URL}\n")

    suite = unittest.TestLoader().loadTestsFromTestCase(WebsiteQATestSuite)
    runner = unittest.TextTestRunner(verbosity=2, resultclass=DetailedTestResult)
    result = runner.run(suite)

    results_data = {
        "total": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures) + len(result.errors),
        "details": result.test_records
    }

    report_path = os.path.join(os.path.dirname(__file__), "test_report.pdf")
    generate_pdf_test_report(results_data, TARGET_URL, report_path)


if __name__ == "__main__":
    run_tests_and_report()
