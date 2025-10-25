# Deploy TenGuard Watch to Cloudflare Pages with Auto-Updates

This guide shows you how to deploy your website to Cloudflare Pages with automatic daily news updates.

## 🚀 Quick Setup (5 minutes)

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit with TenGuard Watch automation"

# Add your GitHub repository (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Connect to Cloudflare Pages

1. **Go to Cloudflare Dashboard**
   - Visit [dash.cloudflare.com](https://dash.cloudflare.com)
   - Navigate to **Pages** in the sidebar

2. **Create New Project**
   - Click **"Create a project"**
   - Choose **"Connect to Git"**
   - Select your GitHub repository

3. **Configure Build Settings**
   - **Project name**: `tenguard-watch` (or your preferred name)
   - **Production branch**: `main`
   - **Build command**: `echo "Static site - no build needed"`
   - **Build output directory**: `/` (root directory)
   - **Root directory**: `/` (leave empty)

4. **Deploy**
   - Click **"Save and Deploy"**
   - Wait for the initial deployment to complete

### Step 3: Verify Auto-Updates

1. **Check GitHub Actions**
   - Go to your GitHub repository
   - Click **"Actions"** tab
   - You should see the workflow running

2. **Test Manual Update**
   - Go to **Actions** → **Update News and Deploy**
   - Click **"Run workflow"** → **"Run workflow"**
   - This will trigger an immediate update

3. **Check Cloudflare Pages**
   - Go back to Cloudflare Pages dashboard
   - You should see a new deployment triggered automatically

## 🔄 How It Works

### Daily Automation Flow:
1. **GitHub Actions runs daily at 9 AM UTC**
2. **Fetches latest news** from Hacker News, SecurityWeek, Dark Reading
3. **Updates `tenguardwatch.html`** with fresh content
4. **Commits and pushes changes** to GitHub
5. **Cloudflare Pages detects changes** and automatically rebuilds
6. **Your website updates** with latest news automatically

### Manual Triggers:
- **GitHub Actions**: Go to Actions tab → "Run workflow"
- **Cloudflare Pages**: Go to Pages dashboard → "Retry deployment"

## 📊 Monitoring

### Check Update Status:
```bash
# View recent logs
tail -20 news_updater.log

# Check last update info
cat update_info.json
```

### GitHub Actions Logs:
1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on the latest workflow run
4. View detailed logs

### Cloudflare Pages Logs:
1. Go to Cloudflare Pages dashboard
2. Click on your project
3. View deployment logs

## 🛠️ Customization

### Change Update Frequency:
Edit `.github/workflows/update-and-deploy.yml`:
```yaml
schedule:
  # Every 6 hours: '0 */6 * * *'
  # Every 12 hours: '0 */12 * * *'
  # Every day at 9 AM: '0 9 * * *'
  - cron: '0 9 * * *'
```

### Add More News Sources:
Edit `auto_news_updater.py` and add new functions like:
```python
def fetch_new_source():
    # Your scraping logic here
    return articles
```

### Custom Domain:
1. Go to Cloudflare Pages dashboard
2. Click **"Custom domains"**
3. Add your domain
4. Update DNS records as instructed

## 🚨 Troubleshooting

### Common Issues:

**1. GitHub Actions not running:**
- Check if the workflow file is in `.github/workflows/`
- Ensure the file has proper YAML syntax
- Check GitHub repository settings

**2. Cloudflare Pages not updating:**
- Verify the repository is connected
- Check build settings are correct
- Look at deployment logs for errors

**3. News not updating:**
- Check GitHub Actions logs
- Verify Python dependencies are installed
- Check if news sources are accessible

**4. Build failures:**
- Ensure all files are committed to GitHub
- Check for syntax errors in Python scripts
- Verify file permissions

### Debug Commands:
```bash
# Test automation locally
python3 auto_news_updater.py

# Check status
python3 check_status.py

# View logs
tail -f news_updater.log
```

## 📈 Benefits

- ✅ **Fully Automated**: No manual intervention needed
- ✅ **Global CDN**: Fast loading worldwide via Cloudflare
- ✅ **Free Hosting**: No server costs
- ✅ **Automatic SSL**: HTTPS enabled by default
- ✅ **Version Control**: Full history of changes
- ✅ **Easy Rollback**: Revert to previous versions instantly
- ✅ **Custom Domain**: Use your own domain name
- ✅ **Analytics**: Built-in Cloudflare analytics

## 🔧 Advanced Features

### Environment Variables:
Add to Cloudflare Pages settings:
- `PYTHON_VERSION`: `3.9`
- `UPDATE_SCHEDULE`: `0 9 * * *`

### Custom Build Commands:
If you need preprocessing:
```yaml
build_command: |
  python3 auto_news_updater.py
  # Add any other build steps here
```

### Multiple Environments:
- **Production**: `main` branch
- **Staging**: `develop` branch
- **Preview**: Pull request deployments

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Verify Cloudflare Pages settings
3. Test automation locally first
4. Check file permissions and syntax

Your TenGuard Watch website will now automatically update daily with the latest cybersecurity news and deploy to Cloudflare Pages without any manual intervention!
