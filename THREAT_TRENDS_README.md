# TenGuard Threat Trends Dashboard

Automated cybersecurity threat intelligence dashboard that aggregates daily news feeds into visual analytics and insights.

## 📊 Features

- **Automated Metrics Computation**: Daily aggregation of threat data from news feeds
- **Interactive Dashboard**: Beautiful, responsive web interface with Chart.js visualizations
- **Trend Analysis**: 7-day and 30-day trend tracking for tags, urgency, sources, and keywords
- **Top Threats**: Automatically surfaces the most critical security articles
- **Lead Generation**: Built-in CTA and email capture form
- **Static Generation**: No server required - works with GitHub Pages
- **Comprehensive Testing**: Full pytest test suite included

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Generate Sample Data** (for testing)

```bash
python scripts/generate_trends.py --sample
```

3. **Generate Metrics from Real Data**

```bash
python scripts/generate_trends.py --days 30
```

4. **Render Dashboard**

```bash
python scripts/render_dashboard.py
```

5. **Preview Locally**

```bash
# Serve the site locally
python -m http.server 8000

# Open browser to:
# http://localhost:8000/threat-trends/
```

## 📁 Project Structure

```
ten-guard-watch/
├── news/                          # Daily news JSON files
│   └── YYYY-MM-DD.json           # Format: {"date": "...", "items": [...]}
├── stats/                         # Generated metrics
│   ├── trends.json               # Latest aggregated metrics
│   └── trends-YYYY-MM-DD.json    # Archived daily snapshots
├── threat-trends/                 # Generated dashboard
│   └── index.html                # Static dashboard page
├── scripts/
│   ├── generate_trends.py        # Metrics computation script
│   └── render_dashboard.py       # Dashboard HTML generator
├── templates/
│   └── threat_trends.j2          # Jinja2 template for dashboard
├── tests/
│   └── test_generate_trends.py   # Pytest test suite
├── .github/workflows/
│   └── generate-trends.yml       # GitHub Actions workflow
├── requirements.txt               # Production dependencies
└── requirements-dev.txt           # Development dependencies
```

## 📝 News JSON Format

Each daily news file should follow this structure:

```json
{
  "date": "2025-01-27",
  "items": [
    {
      "title": "Critical Windows Vulnerability Exploited",
      "link": "https://example.com/article",
      "summary": "A critical vulnerability allows remote code execution...",
      "tags": ["vulnerability", "windows", "exploit"],
      "urgency": "High",
      "slug": "windows-vulnerability-2025",
      "source": "SecurityWeek"
    }
  ]
}
```

### Required Fields

- `title` (string): Article headline
- `link` (string): URL to full article
- `summary` (string): Brief description
- `tags` (array): Category tags
- `urgency` (string): "High", "Medium", or "Low"
- `slug` (string): URL-friendly identifier

### Optional Fields

- `source` (string): News source name (auto-detected from link if not provided)
- `date` (string): Publication date (YYYY-MM-DD format)

## 🔧 Command Line Usage

### Generate Trends

```bash
# Generate with default 30-day lookback
python scripts/generate_trends.py

# Custom date range
python scripts/generate_trends.py --days 7
python scripts/generate_trends.py --days 90

# Generate sample data for testing
python scripts/generate_trends.py --sample
```

### Render Dashboard

```bash
# Render dashboard HTML from trends.json
python scripts/render_dashboard.py

# Set custom webhook URL via environment variable
WEBHOOK_URL="https://hooks.zapier.com/hooks/catch/YOUR_ID/" python scripts/render_dashboard.py
```

## 🧪 Testing

### Run All Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_generate_trends.py -v

# Run specific test
pytest tests/test_generate_trends.py::TestExtractKeywords::test_extract_keywords_basic -v
```

### Test Coverage

The test suite covers:
- ✅ Domain extraction from URLs
- ✅ Keyword extraction and filtering
- ✅ News file loading and parsing
- ✅ Metrics computation (tags, urgency, keywords, etc.)
- ✅ Handling of malformed/missing data
- ✅ Full integration pipeline

## 🤖 GitHub Actions Setup

### 1. Add the Workflow

The workflow file is already created at `.github/workflows/generate-trends.yml`.

### 2. Configure Repository Secrets

Add the following secret in your GitHub repository:

1. Go to **Repository Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:
   - **Name**: `WEBHOOK_URL`
   - **Value**: Your Zapier webhook URL (e.g., `https://hooks.zapier.com/hooks/catch/12345/abcdef/`)

### 3. Enable Workflow Permissions

1. Go to **Repository Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. Click **Save**

### 4. Workflow Schedule

The workflow runs daily at **9:15 AM UTC** (15 minutes after your news scraper):

- **Winter (EST)**: 4:15 AM Eastern
- **Summer (EDT)**: 5:15 AM Eastern

To adjust the schedule, edit the cron expression in `.github/workflows/generate-trends.yml`:

```yaml
schedule:
  - cron: '15 9 * * *'  # Modify this line
```

### 5. Manual Trigger

You can manually trigger the workflow:

1. Go to **Actions** tab
2. Select **Generate Threat Trends Dashboard**
3. Click **Run workflow**

## 📈 Metrics Explained

### Tag Counts
Frequency of each tag/category over 7 and 30 days.

**Example**: `{"malware": 45, "ransomware": 38, "phishing": 35}`

### Urgency Counts
Distribution of threat urgency levels.

**Example**: `{"High": 25, "Medium": 40, "Low": 15}`

### Top Sources
Most frequent news sources by article count.

**Example**: `{"thehackernews.com": 30, "securityweek.com": 25}`

### Top Keywords
Most common keywords extracted from titles and summaries (stopwords filtered).

**Example**: `{"vulnerability": 45, "attack": 40, "breach": 35}`

### Daily Counts
Number of articles per day for the last 30 days.

**Example**: `[{"date": "2025-01-27", "count": 5}, ...]`

### Top Articles
Top 10 articles sorted by urgency (High > Medium > Low) then recency.

## 🎨 Dashboard Customization

### Modify Colors

Edit `templates/threat_trends.j2` and update the `chartColors` object:

```javascript
const chartColors = {
    primary: '#667eea',    // Main brand color
    secondary: '#764ba2',  // Secondary color
    success: '#28a745',    // Low urgency
    warning: '#ffc107',    // Medium urgency
    danger: '#dc3545',     // High urgency
    info: '#17a2b8'
};
```

### Change Chart Types

In the template, modify the `type` parameter:

```javascript
new Chart(ctx, {
    type: 'bar',  // Options: 'bar', 'line', 'pie', 'doughnut', 'radar'
    // ...
});
```

### Add Custom Sections

Add new sections to `templates/threat_trends.j2`:

```html
<div class="custom-section">
    <h2>My Custom Section</h2>
    <!-- Your content here -->
</div>
```

## 🔌 Webhook Integration

### Zapier Setup

1. **Create a Zap**:
   - Trigger: **Webhooks by Zapier** → **Catch Hook**
   - Action: Your choice (e.g., **Gmail** → **Send Email**, **Google Sheets** → **Create Row**)

2. **Get Webhook URL**:
   - Copy the webhook URL from Zapier
   - Example: `https://hooks.zapier.com/hooks/catch/12345/abcdef/`

3. **Add to GitHub Secrets**:
   - Repository Settings → Secrets → New secret
   - Name: `WEBHOOK_URL`
   - Value: Your webhook URL

4. **Test**:
   - Submit the email form on your dashboard
   - Check that the Zap triggers successfully

### Email Capture Data Format

The form sends JSON data:

```json
{
  "email": "user@example.com"
}
```

## 🐛 Troubleshooting

### No Data in Dashboard

**Problem**: Dashboard shows "No Data Yet"

**Solutions**:
1. Check that `news/` directory contains JSON files
2. Verify JSON files follow the correct format
3. Run `python scripts/generate_trends.py --days 30` manually
4. Check logs for parsing errors

### Workflow Fails to Commit

**Problem**: GitHub Actions workflow completes but doesn't commit changes

**Solutions**:
1. Enable **Read and write permissions** in repository settings
2. Check that files were actually generated (look at workflow logs)
3. Verify `stefanzweifel/git-auto-commit-action` has proper permissions

### Charts Not Displaying

**Problem**: Dashboard loads but charts are blank

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify `stats/trends.json` exists and is valid JSON
3. Ensure Chart.js CDN is accessible
4. Check that data arrays are not empty

### Import Errors

**Problem**: `ModuleNotFoundError` when running scripts

**Solutions**:
```bash
# Install all dependencies
pip install -r requirements.txt

# For development/testing
pip install -r requirements-dev.txt

# Verify installation
pip list | grep -E "jinja2|pytest|beautifulsoup4"
```

### Malformed JSON

**Problem**: Script fails to parse news JSON files

**Solutions**:
1. Validate JSON files: `python -m json.tool news/2025-01-27.json`
2. Check for trailing commas, missing quotes, etc.
3. The script logs which files fail to parse

## 📊 Performance Considerations

### Large Datasets

For repositories with 1000+ news articles:

1. **Limit Lookback Period**:
   ```bash
   python scripts/generate_trends.py --days 30  # Instead of 90
   ```

2. **Optimize Keyword Extraction**:
   - Increase `min_length` in `extract_keywords()` function
   - Reduce `top_keywords` count in metrics

3. **Paginate Dashboard**:
   - Modify template to show fewer articles initially
   - Add "Load More" button with JavaScript

### GitHub Actions Timeouts

If the workflow times out:

1. **Reduce Processing**:
   - Lower `--days` parameter
   - Limit number of keywords/tags processed

2. **Optimize File I/O**:
   - Use batch file reading
   - Cache parsed JSON in memory

## 🔐 Security Best Practices

1. **Never commit secrets**: Use GitHub Secrets for webhook URLs
2. **Validate input**: The script sanitizes all user input
3. **Rate limiting**: Respect robots.txt when scraping (script only reads local files)
4. **HTTPS only**: All external links use HTTPS
5. **Content Security Policy**: Consider adding CSP headers if self-hosting

## 📚 Dependencies

### Production
- `requests>=2.28.0`: HTTP library for potential future enhancements
- `beautifulsoup4>=4.11.0`: HTML parsing (for news scraper)
- `lxml>=4.9.0`: Fast XML/HTML parser
- `jinja2>=3.0.0`: Template engine for dashboard generation

### Development
- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Code coverage reporting

### Frontend (CDN)
- Chart.js 4.4.0: Data visualization library

## 🤝 Contributing

### Adding New Metrics

1. **Update `compute_metrics()` in `scripts/generate_trends.py`**:
   ```python
   def compute_metrics(items, days_7, days_30):
       # ... existing code ...
       
       # Add your new metric
       my_metric = calculate_my_metric(items)
       metrics['my_metric'] = my_metric
       
       return metrics
   ```

2. **Update template** in `templates/threat_trends.j2`:
   ```html
   <div class="chart-container">
       <h2>My New Metric</h2>
       <canvas id="myChart"></canvas>
   </div>
   ```

3. **Add tests** in `tests/test_generate_trends.py`:
   ```python
   def test_my_metric():
       items = [...]  # Sample data
       metrics = compute_metrics(items, items, items)
       assert 'my_metric' in metrics
   ```

### Code Style

- Follow PEP 8 for Python code
- Use type hints where practical
- Add docstrings for all functions
- Keep functions focused and testable

## 📄 License

This project is part of TenGuard Security's open-source initiative.

## 🆘 Support

For issues or questions:

1. Check this README first
2. Review the [Troubleshooting](#-troubleshooting) section
3. Check GitHub Actions logs for workflow issues
4. Open an issue in the repository

## 🎯 Roadmap

Future enhancements:

- [ ] RSS feed generation
- [ ] Email digest automation
- [ ] Advanced NLP for entity extraction
- [ ] Threat actor tracking
- [ ] CVE correlation
- [ ] API endpoint for real-time data
- [ ] Mobile app integration
- [ ] Slack/Teams notifications

---

**Last Updated**: January 27, 2025
**Version**: 1.0.0

