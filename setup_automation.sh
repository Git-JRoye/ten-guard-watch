#!/bin/bash

# Setup script for automated news updates
echo "Setting up automated news updates for TenGuard Watch..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Make the script executable
chmod +x auto_news_updater.py

# Create a test run
echo "Testing the news updater..."
python3 auto_news_updater.py

# Set up cron job for weekly updates (every Monday at 9 AM)
echo "Setting up automated daily updates..."
(crontab -l 2>/dev/null; echo "0 9 * * * cd $(pwd) && python3 auto_news_updater.py") | crontab -

echo "Setup complete!"
echo "The news updater will run every day at 9 AM"
echo "You can also run it manually with: python3 auto_news_updater.py"
echo "Check the news_updater.log file for update history"
