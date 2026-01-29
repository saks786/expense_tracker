"""
Convenient test runner script
Runs all tests with proper configuration and reporting
"""
import sys
import subprocess
import time
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000"
BACKEND_DIR = Path(__file__).parent


def check_server():
    """Check if backend server is running"""
    print("Checking if backend server is running...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✓ Backend server is running\n")
            return True
    except requests.exceptions.ConnectionError:
        pass
    
    print("❌ Backend server is not running!")
    print("\nPlease start the backend server first:")
    print("  python -m uvicorn app.main:app --reload")
    print("\nOr run this script with --start-server flag")
    return False


def install_dependencies():
    """Install testing dependencies"""
    print("Installing testing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "pytest", "pytest-cov", "pytest-asyncio", "requests"
    ])
    print("✓ Dependencies installed\n")


def run_tests(test_type="all", coverage=False, verbose=True):
    """
    Run tests with specified configuration
    
    Args:
        test_type: "all", "backend", "e2e", or specific test file
        coverage: Whether to generate coverage report
        verbose: Whether to show verbose output
    """
    print("="*70)
    print("RUNNING TESTS")
    print("="*70)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Determine which tests to run
    if test_type == "all":
        cmd.append("tests/")
    elif test_type == "backend":
        cmd.append("tests/test_backend.py")
    elif test_type == "e2e":
        cmd.append("tests/test_e2e.py")
    else:
        cmd.append(test_type)
    
    # Add options
    if verbose:
        cmd.extend(["-v", "-s"])
    
    if coverage:
        cmd.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    cmd.extend(["--tb=short", "--color=yes"])
    
    # Run tests
    print(f"\nCommand: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=BACKEND_DIR)
    
    print("\n" + "="*70)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*70)
    
    if coverage and result.returncode == 0:
        print("\n📊 Coverage report generated: htmlcov/index.html")
    
    return result.returncode


def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Expense Tracker Backend Tests")
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["all", "backend", "e2e"],
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--coverage",
        "-c",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--install",
        "-i",
        action="store_true",
        help="Install testing dependencies before running"
    )
    parser.add_argument(
        "--skip-server-check",
        action="store_true",
        help="Skip backend server check"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("EXPENSE TRACKER - TEST SUITE")
    print("="*70 + "\n")
    
    # Install dependencies if requested
    if args.install:
        install_dependencies()
    
    # Check if server is running (unless skipped)
    if not args.skip_server_check:
        if not check_server():
            return 1
    
    # Run tests
    return run_tests(
        test_type=args.test_type,
        coverage=args.coverage,
        verbose=True
    )


if __name__ == "__main__":
    sys.exit(main())
