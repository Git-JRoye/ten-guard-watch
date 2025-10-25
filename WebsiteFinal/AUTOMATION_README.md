# TenGuard Watch News Automation

This system automatically updates your TenGuard Watch page with the latest cybersecurity news from The Hacker News, Dark Reading, and SecurityWeek.

## 🚀 Quick Setup

### Option 1: Local Automation (Recommended for personal use)

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup_automation.sh
   ./setup_automation.sh
   ```

3. **Manual test:**
   ```bash
   python3 auto_news_updater.py
   ```

### Option 2: GitHub Actions (Recommended for hosted websites)

1. **Push your code to GitHub**
2. **The automation will run automatically every day at 9 AM UTC**
3. **Changes will be automatically committed and pushed**

## 📋 Features

- ✅ **Automated scraping** from The Hacker News, Dark Reading, and SecurityWeek
- ✅ **Error handling** with detailed logging
- ✅ **Automatic backups** before each update
- ✅ **Daily scheduling** (every day at 9 AM)
- ✅ **Manual triggering** when needed
- ✅ **Status monitoring** and logging
- ✅ **Cloud-based automation** via GitHub Actions

## 🛠️ Manual Usage

### Update news manually:
```bash
python3 auto_news_updater.py
```

### Check update status:
```bash
python3 check_status.py
```

### View logs:
```bash
tail -f news_updater.log
```

## 📅 Scheduling Options

### Local Cron Job
- **Frequency:** Every day at 9 AM
- **Command:** `0 9 * * 1 cd /path/to/your/website && python3 auto_news_updater.py`

### GitHub Actions
- **Frequency:** Every day at 9 AM UTC
- **Automatic:** Commits and pushes changes
- **Manual:** Can be triggered from GitHub interface

## 🔧 Configuration

### Change update frequency:
Edit the cron expression in `setup_automation.sh`:
```bash
# Daily at 9 AM: "0 9 * * *"
# Weekly on Monday: "0 9 * * 1"
# Every 3 days: "0 9 */3 * *"
```

### Change timezone (GitHub Actions):
Edit `.github/workflows/update-news.yml`:
```yaml
- cron: '0 9 * * 1'  # UTC time
```

## 📊 Monitoring

### Check last update:
```bash
python3 check_status.py
```

### View recent logs:
```bash
tail -20 news_updater.log
```

### Check backup files:
```bash
ls -la *.backup_*
```

## 🚨 Troubleshooting

### Common Issues:

1. **"No articles fetched"**
   - Check internet connection
   - Verify website structure hasn't changed
   - Check logs for specific errors

2. **"HTML file not found"**
   - Ensure `tenguardwatch.html` exists in the same directory
   - Check file permissions

3. **"Cron job not running"**
   - Check cron service: `sudo systemctl status cron`
   - Verify cron job: `crontab -l`
   - Check system logs: `journalctl -u cron`

### Recovery:
If something goes wrong, the system creates automatic backups:
```bash
# Restore from backup
cp tenguardwatch.html.backup_YYYYMMDD_HHMMSS tenguardwatch.html
```

## 📁 File Structure

```
├── auto_news_updater.py      # Main automation script
├── check_status.py           # Status monitoring
├── setup_automation.sh       # Setup script
├── requirements.txt          # Python dependencies
├── news_updater.log          # Automation logs
├── update_info.json          # Update metadata
├── tenguardwatch.html        # Your website file
└── .github/workflows/        # GitHub Actions
    └── update-news.yml
```

## 🔄 Update Process

1. **Backup** current HTML file
2. **Fetch** latest articles from news sources
3. **Parse** and format content
4. **Update** HTML with new content
5. **Log** the update with metadata
6. **Commit** changes (if using GitHub Actions)

## 📈 Benefits

- **Time-saving:** No more manual weekly updates
- **Reliable:** Automated error handling and backups
- **Fresh content:** Always up-to-date with latest news
- **Monitoring:** Easy status checking and logging
- **Flexible:** Multiple deployment options

## 🆘 Support

If you encounter issues:
1. Check the logs: `news_updater.log`
2. Run status check: `python3 check_status.py`
3. Test manually: `python3 auto_news_updater.py`
4. Check backup files for recovery
