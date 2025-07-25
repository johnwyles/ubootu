#!/bin/bash
# Run all checks exactly as GitHub Actions does
# This ensures local testing matches CI/CD

set -e  # Exit on first error

echo "================================================"
echo "Running ALL checks (matching GitHub Actions)"
echo "================================================"

# Activate virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

# Track failures
FAILED=0

echo ""
echo "1. Running yamllint..."
echo "------------------------"
if yamllint .; then
    echo "✓ yamllint passed"
else
    echo "✗ yamllint failed"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "2. Running ansible-lint..."
echo "------------------------"
if ansible-lint; then
    echo "✓ ansible-lint passed"
else
    echo "✗ ansible-lint failed"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "3. Running flake8..."
echo "------------------------"
if flake8 lib/ configure_standard_tui.py --max-line-length=120; then
    echo "✓ flake8 passed"
else
    echo "✗ flake8 failed"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "4. Running black (check mode)..."
echo "------------------------"
if black --check lib/ configure_standard_tui.py tests/; then
    echo "✓ black passed"
else
    echo "✗ black failed (run 'black lib/ configure_standard_tui.py tests/' to fix)"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "5. Running isort (check mode)..."
echo "------------------------"
if isort --check-only lib/ configure_standard_tui.py tests/; then
    echo "✓ isort passed"
else
    echo "✗ isort failed (run 'isort lib/ configure_standard_tui.py tests/' to fix)"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "6. Running pytest with coverage..."
echo "------------------------"
if pytest tests/ -vv --tb=long --cov --cov-report=xml --cov-report=term-missing; then
    echo "✓ pytest passed"
else
    echo "✗ pytest failed"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "================================================"
if [ $FAILED -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED! Safe to push to GitHub."
else
    echo "❌ $FAILED check(s) failed. Fix issues before pushing."
    exit 1
fi
echo "================================================"