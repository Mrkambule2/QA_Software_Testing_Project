import os
import sys
import subprocess

def run_all():
    print("=" * 65)
    print("        AUTOMATED SOFTWARE TESTING & PDF GENERATOR SUITE")
    print("=" * 65)

    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Prompt user for Target Website / API URL
    target_url = ""
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        target_url = sys.argv[1]
    else:
        user_input = input("\nEnter Target Website / API URL to test (Press Enter for default 'https://httpbin.org'): ").strip()
        if user_input:
            target_url = user_input if user_input.startswith("http") else "https://" + user_input
        else:
            target_url = "https://httpbin.org"

    print(f"\nTarget set to: {target_url}")

    # 1. Generate PDF Guide
    print("\n[Step 1/2] Generating Software Testing Guide PDF...")
    guide_script = os.path.join(project_dir, "generate_qa_guide_pdf.py")
    res1 = subprocess.run([sys.executable, guide_script], capture_output=True, text=True)
    print(res1.stdout)
    if res1.returncode != 0:
        print("[ERROR] Failed to generate PDF Guide:", res1.stderr)

    # 2. Execute Test Suite & Generate Test Report PDF
    print("\n[Step 2/2] Executing Automated QA Test Suite & Generating Test Report PDF...")
    test_script = os.path.join(project_dir, "test_suite.py")
    res2 = subprocess.run([sys.executable, test_script, target_url], capture_output=True, text=True)
    print(res2.stdout)
    if res2.returncode != 0:
        print("[ERROR] Test suite execution failed:", res2.stderr)

    print("\n" + "=" * 65)
    print("  SUCCESS: ALL SCRIPTS EXECUTED & PDF REPORTS CREATED ON DESKTOP")
    print("=" * 65)
    print(f" Project Folder Path: {project_dir}")
    print(f" Tested URL: {target_url}")
    print(" Generated PDF Documents:")
    print(f"   - {os.path.join(project_dir, 'Software_Testing_Guide.pdf')}")
    print(f"   - {os.path.join(project_dir, 'test_report.pdf')}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_all()
