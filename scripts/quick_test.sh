#!/bin/bash
# Quick test script for Threat Trends Dashboard
# Usage: bash scripts/quick_test.sh

set -e  # Exit on error

echo "🚀 TenGuard Threat Trends - Quick Test"
echo "======================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed"
    exit 1
fi

echo "✅ pip found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q jinja2 pytest 2>/dev/null || pip3 install -q jinja2 pytest 2>/dev/null
echo "✅ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
if python3 -m pytest tests/ -v --tb=short; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed"
    exit 1
fi
echo ""

# Generate sample data
echo "📊 Generating sample data..."
python3 scripts/generate_trends.py --sample
echo "✅ Sample data generated"
echo ""

# Generate metrics from sample news
echo "📈 Generating metrics from sample news..."
python3 scripts/generate_trends.py --days 30
echo "✅ Metrics generated"
echo ""

# Render dashboard
echo "🎨 Rendering dashboard..."
python3 scripts/render_dashboard.py
echo "✅ Dashboard rendered"
echo ""

# Check generated files
echo "📁 Checking generated files..."
if [ -f "stats/trends.json" ]; then
    echo "  ✅ stats/trends.json ($(du -h stats/trends.json | cut -f1))"
else
    echo "  ❌ stats/trends.json not found"
    exit 1
fi

if [ -f "threat-trends/index.html" ]; then
    echo "  ✅ threat-trends/index.html ($(du -h threat-trends/index.html | cut -f1))"
else
    echo "  ❌ threat-trends/index.html not found"
    exit 1
fi
echo ""

# Success message
echo "🎉 Success! All tests passed and dashboard generated."
echo ""
echo "📋 Next steps:"
echo "  1. Preview dashboard: python3 -m http.server 8000"
echo "  2. Open browser: http://localhost:8000/threat-trends/"
echo "  3. Review files in stats/ and threat-trends/ directories"
echo ""
echo "🚀 Ready to deploy!"

