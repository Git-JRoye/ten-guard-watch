#!/usr/bin/env python3
"""
Status checker for TenGuard Watch news automation
"""

import json
import os
from datetime import datetime, timedelta

def check_update_status():
    """Check the status of the last update"""
    if not os.path.exists("update_info.json"):
        print("❌ No update information found. Run the updater first.")
        return
    
    with open("update_info.json", "r") as f:
        info = json.load(f)
    
    last_update = datetime.fromisoformat(info["last_update"])
    articles_count = info["articles_count"]
    backup_file = info.get("backup_file", "N/A")
    
    print("📊 TenGuard Watch News Status")
    print("=" * 40)
    print(f"Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Articles Count: {articles_count}")
    print(f"Backup File: {backup_file}")
    
    # Check if update is recent (within last 7 days)
    days_since_update = (datetime.now() - last_update).days
    if days_since_update <= 7:
        print(f"✅ Status: Fresh (updated {days_since_update} days ago)")
    elif days_since_update <= 14:
        print(f"⚠️  Status: Stale (updated {days_since_update} days ago)")
    else:
        print(f"❌ Status: Outdated (updated {days_since_update} days ago)")
        print("   Consider running the updater manually.")

def check_logs():
    """Check recent log entries"""
    if not os.path.exists("news_updater.log"):
        print("❌ No log file found.")
        return
    
    print("\n📋 Recent Log Entries:")
    print("-" * 40)
    
    with open("news_updater.log", "r") as f:
        lines = f.readlines()
        # Show last 10 lines
        for line in lines[-10:]:
            print(line.strip())

if __name__ == "__main__":
    check_update_status()
    check_logs()
