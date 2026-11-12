# QA Software Testing Project & Automated PDF Suite

This project contains automated software QA testing scripts and PDF documentation generators.

---

## Folder Location
`C:\Users\pc\Desktop\QA_Software_Testing_Project`

---

## File Overview

1. **`run_all_qa_tests.py`**: Master runner script. Executes the automated test suite and builds all PDF documentation in one step.
2. **`test_suite.py`**: Automated QA test suite covering API status codes, schema validation, bad input handling, latency benchmarking, and automated PDF test report output (`test_report.pdf`).
3. **`generate_qa_guide_pdf.py`**: Script that generates `Software_Testing_Guide.pdf` detailing setup, test execution commands, and developer bug reporting protocols.
4. **`Software_Testing_Guide.pdf`**: Generated PDF guide explaining how to run test scripts and report findings to development teams.
5. **`test_report.pdf`**: Generated PDF execution report containing pass/fail metrics and test case logs.

---

## How to Run

Open Command Prompt or Terminal, navigate to this directory, and run:

```bash
cd C:\Users\pc\Desktop\QA_Software_Testing_Project
python run_all_qa_tests.py
```

Or run individual scripts:

```bash
# Run test suite and generate test_report.pdf
python test_suite.py

# Generate Software_Testing_Guide.pdf
python generate_qa_guide_pdf.py
```
