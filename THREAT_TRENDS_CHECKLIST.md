# 🎯 TenGuard Threat Trends Dashboard - Implementation Checklist

## ✅ Files Created

### Core Scripts
- [x] `scripts/generate_trends.py` - Main metrics computation engine
- [x] `scripts/render_dashboard.py` - Dashboard HTML renderer

### Templates
- [x] `templates/threat_trends.j2` - Jinja2 template for dashboard page

### Tests
- [x] `tests/test_generate_trends.py` - Comprehensive pytest test suite
- [x] `news/sample-2025-01-27.json` - Sample news data for testing

### Workflows
- [x] `.github/workflows/generate-trends.yml` - GitHub Actions automation

### Documentation
- [x] `THREAT_TRENDS_README.md` - Complete usage documentation
- [x] `THREAT_TRENDS_CHECKLIST.md` - This implementation checklist

### Dependencies
- [x] `requirements.txt` - Updated with jinja2
- [x] `requirements-dev.txt` - Testing dependencies

---

## 📋 Setup Instructions

### 1. Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# For development/testing
pip install -r requirements-dev.txt

# Test the installation
python scripts/generate_trends.py --sample
python scripts/render_dashboard.py
```

### 2. GitHub Repository Secrets

Add the following secret to your GitHub repository:

**Go to**: Repository Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `WEBHOOK_URL` | Zapier webhook URL for email capture | `https://hooks.zapier.com/hooks/catch/12345/abcdef/` |

**Steps**:
1. Navigate to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Name: `WEBHOOK_URL`
6. Value: Your Zapier webhook URL
7. Click **Add secret**

### 3. Enable GitHub Actions Permissions

**Go to**: Repository Settings → Actions → General → Workflow permissions

**Configure**:
- ✅ Select **Read and write permissions**
- ✅ Check **Allow GitHub Actions to create and approve pull requests**
- Click **Save**

### 4. Verify Directory Structure

Ensure these directories exist (they'll be auto-created if missing):

```
ten-guard-watch/
├── news/              # Your daily news JSON files go here
├── stats/             # Auto-generated metrics (created by script)
├── threat-trends/     # Auto-generated dashboard (created by script)
├── scripts/           # Python scripts (already created)
├── templates/         # Jinja2 templates (already created)
└── tests/             # Test files (already created)
```

---

## 🧪 Testing

### Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run specific test
pytest tests/test_generate_trends.py::TestExtractKeywords -v
```

### Test the Full Pipeline

```bash
# 1. Generate sample data
python scripts/generate_trends.py --sample

# 2. Generate metrics from sample
python scripts/generate_trends.py --days 30

# 3. Render dashboard
python scripts/render_dashboard.py

# 4. Preview locally
python -m http.server 8000
# Open: http://localhost:8000/threat-trends/
```

---

## 🚀 Deployment

### Option 1: Automatic (GitHub Actions)

The workflow will run automatically:
- **Daily at 9:15 AM UTC** (15 minutes after your news scraper)
- After every push to `main` branch (if configured)

**Manual Trigger**:
1. Go to **Actions** tab on GitHub
2. Select **Generate Threat Trends Dashboard**
3. Click **Run workflow**
4. Click **Run workflow** button

### Option 2: Manual Local Run

```bash
# Generate trends and dashboard
python scripts/generate_trends.py --days 30
python scripts/render_dashboard.py

# Commit and push
git add stats/ threat-trends/
git commit -m "Update threat trends dashboard"
git push origin main
```

---

## 🔧 Configuration

### Adjust Time Period

Edit `.github/workflows/generate-trends.yml`:

```yaml
- name: Generate trends metrics
  run: |
    python scripts/generate_trends.py --days 30  # Change this number
```

### Change Workflow Schedule

Edit `.github/workflows/generate-trends.yml`:

```yaml
schedule:
  - cron: '15 9 * * *'  # Modify this cron expression
```

**Cron Examples**:
- `'0 9 * * *'` - 9:00 AM UTC daily
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1'` - 9:00 AM UTC every Monday

### Customize Dashboard Colors

Edit `templates/threat_trends.j2` and modify:

```javascript
const chartColors = {
    primary: '#667eea',    // Your brand color
    secondary: '#764ba2',  // Secondary color
    // ... etc
};
```

### Change Email Webhook

**Option 1**: Update GitHub Secret
- Go to Repository Settings → Secrets → `WEBHOOK_URL`
- Update the value

**Option 2**: Set Environment Variable Locally
```bash
export WEBHOOK_URL="https://hooks.zapier.com/hooks/catch/YOUR_NEW_ID/"
python scripts/render_dashboard.py
```

---

## 📊 Data Format

### News JSON Structure

Your daily news files in `news/YYYY-MM-DD.json` should follow this format:

```json
{
  "date": "2025-01-27",
  "items": [
    {
      "title": "Article Title",
      "link": "https://example.com/article",
      "summary": "Brief description of the threat...",
      "tags": ["vulnerability", "windows", "critical"],
      "urgency": "High",
      "slug": "article-slug",
      "source": "SecurityWeek"
    }
  ]
}
```

**Required Fields**:
- `title` (string)
- `link` (string)
- `summary` (string)
- `tags` (array of strings)
- `urgency` ("High", "Medium", or "Low")
- `slug` (string)

**Optional Fields**:
- `source` (string) - Auto-detected from link if not provided
- `date` (string) - Auto-added if not present

---

## 🎨 Customization Points

### 1. Add New Metrics

**File**: `scripts/generate_trends.py`

```python
def compute_metrics(items, days_7, days_30):
    # ... existing code ...
    
    # Add your custom metric
    metrics['my_custom_metric'] = calculate_my_metric(items)
    
    return metrics
```

### 2. Add New Charts

**File**: `templates/threat_trends.j2`

```html
<div class="chart-container">
    <h2>My Custom Chart</h2>
    <div class="chart-wrapper">
        <canvas id="myCustomChart"></canvas>
    </div>
</div>

<script>
const myCtx = document.getElementById('myCustomChart').getContext('2d');
new Chart(myCtx, {
    type: 'bar',
    data: {
        labels: {{ my_labels|tojson }},
        datasets: [{
            label: 'My Data',
            data: {{ my_values|tojson }}
        }]
    }
});
</script>
```

### 3. Modify Dashboard Layout

**File**: `templates/threat_trends.j2`

- Rearrange sections by moving HTML blocks
- Add custom CSS in the `<style>` section
- Modify grid layouts (`.chart-grid`, `.kpi-grid`)

---

## 🐛 Troubleshooting

### Issue: Workflow Fails to Run

**Check**:
1. Workflow permissions are set to "Read and write"
2. Workflow file is in `.github/workflows/` directory
3. YAML syntax is valid (use a YAML validator)

**Fix**:
```bash
# Validate YAML locally
python -c "import yaml; yaml.safe_load(open('.github/workflows/generate-trends.yml'))"
```

### Issue: No Data in Dashboard

**Check**:
1. `news/` directory contains JSON files
2. JSON files follow the correct format
3. `stats/trends.json` was generated

**Fix**:
```bash
# Check news files
ls -la news/

# Validate JSON
python -m json.tool news/2025-01-27.json

# Generate manually
python scripts/generate_trends.py --days 30
```

### Issue: Charts Not Displaying

**Check**:
1. Browser console for JavaScript errors
2. Chart.js CDN is accessible
3. Data arrays are not empty

**Fix**:
- Open browser DevTools (F12)
- Check Console tab for errors
- Verify `stats/trends.json` contains data

### Issue: Import Errors

**Fix**:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify installation
pip list | grep -E "jinja2|pytest"
```

---

## 📈 Monitoring

### Check Workflow Status

1. Go to **Actions** tab on GitHub
2. View recent workflow runs
3. Click on a run to see detailed logs

### View Generated Files

After workflow runs:
- `stats/trends.json` - Latest metrics
- `stats/trends-YYYY-MM-DD.json` - Daily archive
- `threat-trends/index.html` - Dashboard page

### Monitor Metrics

Check these indicators:
- ✅ Workflow completes successfully
- ✅ Files are committed to repository
- ✅ Dashboard loads without errors
- ✅ Charts display data correctly

---

## 🔐 Security Checklist

- [x] Secrets stored in GitHub Secrets (not in code)
- [x] Webhook URL not exposed in public files
- [x] Input validation in Python scripts
- [x] No hardcoded credentials
- [x] HTTPS used for all external resources
- [x] Proper error handling for malformed data

---

## 📚 Additional Resources

### Documentation
- [THREAT_TRENDS_README.md](THREAT_TRENDS_README.md) - Complete usage guide
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

### External Dependencies
- Chart.js CDN: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/`
- Zapier Webhooks: `https://zapier.com/apps/webhook/integrations`

---

## ✨ Success Criteria

Your implementation is successful when:

- ✅ Tests pass: `pytest tests/ -v`
- ✅ Sample data generates: `python scripts/generate_trends.py --sample`
- ✅ Dashboard renders: `python scripts/render_dashboard.py`
- ✅ Workflow runs without errors
- ✅ Dashboard displays at `/threat-trends/index.html`
- ✅ Charts show data correctly
- ✅ Email form submits to webhook
- ✅ Daily automation works

---

## 🎉 Next Steps

After successful implementation:

1. **Test the full pipeline** with real news data
2. **Customize the dashboard** colors and branding
3. **Set up Zapier** for email capture
4. **Monitor the first few** automated runs
5. **Share the dashboard** with stakeholders
6. **Collect feedback** and iterate

---

## 📞 Support

If you encounter issues:

1. Review this checklist
2. Check [THREAT_TRENDS_README.md](THREAT_TRENDS_README.md)
3. Review GitHub Actions logs
4. Validate your news JSON format
5. Test scripts locally first

---

**Implementation Date**: January 27, 2025  
**Version**: 1.0.0  
**Status**: ✅ Complete and Ready for Deployment

